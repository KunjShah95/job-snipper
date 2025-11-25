"""
Clean, self-contained Gradio front-end for ResumeMasterAI.
This version is intentionally self-contained for UI/CSS validation and local testing.
- Includes high-contrast, readable CSS
- Uses safe fallbacks for backend service imports (graceful degraded behavior)
- Small demo implementations for parsing/matching so the UI is interactive
"""

import os
import sys
import json
from typing import Optional, Tuple

import gradio as gr
from utils.color_scheme import get_gradio_css

# Attempt to import real services; if not available, provide safe fallbacks
try:
    from services.pdf_parser import parse_pdf
except Exception:
    def parse_pdf(path):
        try:
            with open(path, 'rb') as f:
                return f"(binary PDF content {os.path.basename(path)})"
        except Exception:
            return ""

try:
    from services.docx_parser import parse_docx
except Exception:
    def parse_docx(path):
        try:
            return f"(docx content {os.path.basename(path)})"
        except Exception:
            return ""

# Minimal resume parser fallback
try:
    from services.resume_parser import parse_resume_to_json
except Exception:
    def parse_resume_to_json(raw_text: str):
        # Very simple heuristic parser for demo purposes
        lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
        skills = []
        experience = []
        education = []
        for l in lines:
            low = l.lower()
            if any(k in low for k in ["python", "java", "sql", "aws", "docker"]):
                skills.extend([s.strip() for s in l.split(',')][:5])
            if any(k in low for k in ["engineer", "developer", "manager", "analyst"]):
                experience.append(l)
            if any(k in low for k in ["university", "bachelor", "master", "bs", "ms"]):
                education.append(l)
        return {
            "raw_text": raw_text,
            "skills": list(dict.fromkeys([s for s in skills if s])),
            "experience": experience,
            "education": education,
        }

# Very small matcher fallback
try:
    from services.resume_matcher import match_resume_to_jd
except Exception:
    def match_resume_to_jd(resume_data, job_description):
        # Return a short plain-text summary
        skills = set(resume_data.get('skills', []))
        jd_tokens = set([t.lower() for t in job_description.replace('(', ' ').replace(')', ' ').split()])
        matched = skills.intersection(jd_tokens)
        return f"Matched keywords: {', '.join(matched) if matched else 'None'}"

# Rewriter fallback
try:
    from services.resume_rewriter import rewrite_resume
except Exception:
    def rewrite_resume(resume_json: dict, instruction: str = None) -> dict:
        raw = resume_json.get('raw_text', '')
        # naive rewrite: prefix instruction and return
        return {"rewritten_text": (instruction or "") + "\n\n" + raw}

# Cover letter fallback
try:
    from services.coverletter_gen import generate_cover_letter
except Exception:
    def generate_cover_letter(resume_json, jd_text, tone="formal"):
        return f"Dear Hiring Manager,\n\nBased on the job description: {jd_text[:120]}...\n\nSincerely,\nCandidate"

# Minimal job search fallback
try:
    from services.job_scraper import search_jobs
except Exception:
    def search_jobs(jd_text, max_results=5):
        results = []
        for i in range(max_results):
            results.append({
                "title": f"Software Engineer {i+1}",
                "company": f"Company {i+1}",
                "location": "Remote",
                "match_score": 80 - i,
                "url": "#"
            })
        return results

# Scoring utils
try:
    from utils.scoring_utils import compute_subscores, combine_scores, explain_score
except Exception:
    def compute_subscores(parsed_resume: dict):
        return {"structure": 50.0, "skills": 40.0, "content": 45.0}

    def combine_scores(subscores, weights=None):
        if weights is None:
            weights = {"structure": 0.3, "skills": 0.35, "content": 0.35}
        overall = 0.0
        for k,w in weights.items():
            overall += subscores.get(k, 0.0) * w
        return {"overall": round(overall,2), "breakdown": subscores}

    def explain_score(parsed_resume, subscores):
        return ["Score explanation not available in fallback"]

# ATS Scanner
try:
    from utils.ats_scanner import ATSScanner
except Exception:
    class ATSScanner:
        def scan_resume(self, text, fmt='txt'):
            return {"overall_score": 75, "recommendations": ["Fallback ATS: keep resume simple"]}

# Email generator
try:
    from utils.email_generator import EmailGenerator
except Exception:
    class EmailGenerator:
        def __init__(self):
            pass
        def generate_recruiter_email(self, *args, **kwargs):
            return "Dear Recruiter,\n\nThis is a fallback email.\n"

# CSS — high contrast, readable, compact but modern
custom_css = get_gradio_css()

# Helper: parse uploaded resume

def parse_uploaded_resume(file) -> Tuple[Optional[str], Optional[dict]]:
    if file is None:
        return None, None
    try:
        file_path = file.name
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            text = parse_pdf(file_path)
        elif ext in ['.docx', '.doc']:
            text = parse_docx(file_path)
        else:
            # plain text
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        parsed = parse_resume_to_json(text)
        return text, parsed
    except Exception as e:
        return None, {"error": str(e)}

# Gradio callback functions

def analyze_resume(file):
    if file is None:
        return "❌ Please upload a resume.", "", ""
    text, parsed = parse_uploaded_resume(file)
    if text is None:
        return f"❌ Error: {parsed.get('error', 'Unknown')}", "", ""

    ats_score = 75  # demo
    strengths = ["Clear Skills section", "Good job titles"]
    weaknesses = ["Add metrics to bullets"]
    recommendations = ["Add numbers (e.g., improved X by 20%)"]

    summary = f"## Resume Analysis\n\n- ATS Score: {ats_score}/100\n- Skills detected: {', '.join(parsed.get('skills', [])[:6]) or 'None'}\n- Experience entries: {len(parsed.get('experience', []))}\n"
    parsed_json = json.dumps(parsed, indent=2)
    return summary, text, parsed_json


def match_with_job(resume_file, job_description):
    if resume_file is None:
        return "❌ Please upload a resume."
    if not job_description:
        return "❌ Please add a job description."
    text, parsed = parse_uploaded_resume(resume_file)
    if text is None:
        return "❌ Error parsing resume"
    match = match_resume_to_jd(parsed, job_description)
    score = 80
    summary = f"## Match Score: {score}/100\n\n{match}"
    # attempt to create visualization
    viz_path = None
    try:
        matched_skills = parsed.get('skills', [])
        # naive missing skills: tokens in JD not in resume skills
        jd_tokens = [t.lower().strip('.,()') for t in job_description.split()]
        missing = [t for t in jd_tokens if t and t not in [s.lower() for s in matched_skills]]
        viz_path = create_skill_match_visualization(matched_skills, missing[:10], score)
    except Exception:
        viz_path = None
    return summary, viz_path


def rewrite_resume_content(resume_file, job_description, focus_area):
    if resume_file is None:
        return "❌ Please upload a resume."
    text, parsed = parse_uploaded_resume(resume_file)
    if text is None:
        return "❌ Error parsing resume"
    resume_data = {"raw_text": text, **parsed}
    instruction = f"Focus on {focus_area}. Tailor for: {job_description[:140]}"
    rewritten = rewrite_resume(resume_data, instruction)
    return rewritten.get('rewritten_text', text)


def generate_cover_letter_content(resume_file, job_description, company, position):
    if resume_file is None or not job_description:
        return "❌ Upload resume and provide job details."
    text, parsed = parse_uploaded_resume(resume_file)
    resume_data = {"raw_text": text, **parsed}
    enhanced = f"Company: {company or 'Company'}\nPosition: {position or 'Position'}\n\n{job_description}"
    return generate_cover_letter(resume_data, enhanced)

# Visualization helpers (matplotlib/plotly) from utils.workflow_visual
try:
    from utils.workflow_visual import (
        create_score_visualization,
        create_skill_match_visualization,
        visualize_agents_workflow,
    )
except Exception:
    def create_score_visualization(subscores, overall_score, out_filename: str = "score_visual"):
        # Fallback: no visualization available
        return None

    def create_skill_match_visualization(matched_skills, missing_skills, match_score, out_filename: str = "skill_match"):
        return None

    def visualize_agents_workflow(result_dict, out_filename: str = "workflow_graph"):
        return None

# Build the Gradio interface

def build_interface():
    with gr.Blocks(css=custom_css, title="ResumeMasterAI Demo") as demo:
        # Header
        with gr.Row():
            with gr.Column(scale=1):
                gr.HTML("""
                    <div class='header'>
                        <h1>ResumeMasterAI</h1>
                        <p>An interactive demo - high contrast and readable UI</p>
                    </div>
                """)

        with gr.Tabs():
            with gr.TabItem("Analyze"):
                with gr.Row():
                    with gr.Column(scale=1):
                        resume_file = gr.File(label="Upload Resume (PDF/DOCX/TXT)")
                        analyze_btn = gr.Button("Analyze", variant="primary")
                    with gr.Column(scale=2):
                        analysis_md = gr.Markdown()
                with gr.Accordion("Extracted Text", open=False):
                    extracted = gr.Textbox(lines=8)
                with gr.Accordion("Parsed JSON", open=False):
                    parsed_out = gr.Code(language='json')
                analyze_btn.click(fn=analyze_resume, inputs=[resume_file], outputs=[analysis_md, extracted, parsed_out])

            with gr.TabItem("Match"):
                with gr.Row():
                    with gr.Column():
                        resume_file2 = gr.File(label="Upload Resume")
                        jd = gr.Textbox(label="Job Description", lines=6)
                        match_btn = gr.Button("Match", variant="primary")
                    with gr.Column():
                        match_out = gr.Markdown()
                        match_viz = gr.Image(type='filepath', label="Match Visualization")
                match_btn.click(fn=match_with_job, inputs=[resume_file2, jd], outputs=[match_out, match_viz])

            with gr.TabItem("Rewrite"):
                with gr.Row():
                    with gr.Column():
                        resume_file3 = gr.File(label="Upload Resume")
                        jd2 = gr.Textbox(label="(Optional) Job Description", lines=4)
                        focus = gr.Dropdown(choices=["General", "Technical Skills", "Leadership"], value="General", label="Focus")
                        rewrite_btn = gr.Button("Rewrite", variant="primary")
                    with gr.Column():
                        rewrite_out = gr.Markdown()
                rewrite_btn.click(fn=rewrite_resume_content, inputs=[resume_file3, jd2, focus], outputs=[rewrite_out])

            with gr.TabItem("Cover Letter"):
                with gr.Row():
                    with gr.Column():
                        resume_file4 = gr.File(label="Upload Resume")
                        jd3 = gr.Textbox(label="Job Description", lines=6)
                        company = gr.Textbox(label="Company")
                        position = gr.Textbox(label="Position")
                        cl_btn = gr.Button("Generate", variant="primary")
                    with gr.Column():
                        cl_md = gr.Markdown()
                cl_btn.click(fn=generate_cover_letter_content, inputs=[resume_file4, jd3, company, position], outputs=[cl_md])

            with gr.TabItem("Score"):
                with gr.Row():
                    with gr.Column(scale=1):
                        resume_file_s = gr.File(label="Upload Resume for Scoring")
                        score_btn = gr.Button("Analyze & Score", variant="primary")
                    with gr.Column(scale=2):
                        overall_md = gr.Markdown()
                        breakdown = gr.Code(language='json')
                        score_img = gr.Image(type='filepath', label="Score Visualization")
                def run_scoring(file):
                    if file is None:
                        return "❌ Please upload a resume.", "{}"
                    text, parsed = parse_uploaded_resume(file)
                    if text is None:
                        return "❌ Error parsing resume", "{}"
                    subs = compute_subscores(parsed)
                    comb = combine_scores(subs)
                    expl = explain_score(parsed, subs)
                    summary = f"## Overall Score: {comb['overall']}/100\n\n" + "\n".join([f"- {s}" for s in expl])
                    # Try to create visualization
                    viz_path = None
                    try:
                        viz_path = create_score_visualization(subs, comb['overall'])
                    except Exception:
                        viz_path = None
                    return summary, json.dumps({"subscores": subs, "overall": comb['overall']}, indent=2), viz_path
                score_btn.click(fn=run_scoring, inputs=[resume_file_s], outputs=[overall_md, breakdown, score_img])

            with gr.TabItem("ATS Scanner"):
                with gr.Row():
                    with gr.Column(scale=1):
                        resume_file_ats = gr.File(label="Upload Resume for ATS Scan")
                        ats_btn = gr.Button("Run ATS Scan", variant="primary")
                    with gr.Column(scale=2):
                        ats_md = gr.Markdown()
                        ats_recs = gr.Textbox(lines=8)
                def run_ats(file):
                    if file is None:
                        return "❌ Please upload a resume.", ""
                    text, parsed = parse_uploaded_resume(file)
                    if text is None:
                        return "❌ Error parsing resume", ""
                    scanner = ATSScanner()
                    results = scanner.scan_resume(text)
                    summary = f"## ATS Score: {results.get('overall_score', 'N/A')}/100\n\n"
                    summary += "\n".join(results.get('recommendations', []))
                    return summary, "\n".join(results.get('recommendations', []))

                ats_btn.click(fn=run_ats, inputs=[resume_file_ats], outputs=[ats_md, ats_recs])

            with gr.TabItem("Job Search"):
                with gr.Row():
                    with gr.Column(scale=1):
                        jd_input = gr.Textbox(label="Job Description", lines=6)
                        search_btn = gr.Button("Search Jobs", variant="primary")
                    with gr.Column(scale=2):
                        jobs_out = gr.Dataframe()
                def run_search(jd_text):
                    if not jd_text or not jd_text.strip():
                        return []
                    try:
                        results = search_jobs(jd_text, max_results=8)
                        # If DataFrame-like
                        if hasattr(results, 'to_dict'):
                            return results
                        return results
                    except Exception as e:
                        return []

                search_btn.click(fn=run_search, inputs=[jd_input], outputs=[jobs_out])

            with gr.TabItem("Email"):
                with gr.Row():
                    with gr.Column(scale=1):
                        tone = gr.Dropdown(choices=["professional","casual","confident"], value="professional", label="Tone")
                        recip = gr.Textbox(label="Recipient Name")
                        company_e = gr.Textbox(label="Company")
                        position_e = gr.Textbox(label="Position")
                        your_name = gr.Textbox(label="Your Name")
                        expertise = gr.Textbox(label="Your Expertise")
                        gen_btn = gr.Button("Generate Email", variant="primary")
                    with gr.Column(scale=2):
                        email_out = gr.Textbox(lines=12)

                def gen_email(recipient_name, company_name, position, your_name_v, your_expertise, tone_v):
                    gen = EmailGenerator()
                    return gen.generate_recruiter_email(recipient_name or 'Recruiter', company_name or 'Company', position or 'Position', your_name_v or 'Name', your_expertise or 'Expertise', tone=tone_v)

                gen_btn.click(fn=gen_email, inputs=[recip, company_e, position_e, your_name, expertise, tone], outputs=[email_out])

            with gr.TabItem("Workflow"):
                with gr.Row():
                    with gr.Column(scale=1):
                        run_wf_btn = gr.Button("Generate Workflow Visualization", variant="primary")
                    with gr.Column(scale=2):
                        wf_img = gr.Image(type='filepath', label="Workflow Visualization")

                def run_workflow_viz():
                    # Build a minimal result dict showing which agents produced output
                    result = {
                        "parser": True,
                        "scoring": True,
                        "matcher": True,
                        "rewrite": False,
                        "coverletter": False,
                        "projectsuggester": False,
                        "jobsearch": True,
                    }
                    try:
                        path = visualize_agents_workflow(result, out_filename="workflow_gradio")
                        return path
                    except Exception as e:
                        return None

                run_wf_btn.click(fn=run_workflow_viz, inputs=[], outputs=[wf_img])

        # Footer
        gr.HTML("""
            <div class='footer'>
                <div style='background: linear-gradient(90deg,#ffffff,#f4fbff); padding:16px; border-radius:8px; display:inline-block;'>
                    <strong style='color:#0f1724'>Tips:</strong> Upload clear PDFs/DOCX and provide detailed job descriptions for best results.
                </div>
                <div style='margin-top:12px; font-size:0.95rem; color: #bcd4ff;'>Made with ❤ ResumeMasterAI Demo</div>
            </div>
        """)

    return demo

if __name__ == '__main__':
    demo = build_interface()
    demo.launch(server_name='0.0.0.0', server_port=7862, debug=True)
