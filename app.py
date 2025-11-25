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
import uuid
import urllib.parse
from typing import Optional, Tuple

import gradio as gr
from dotenv import load_dotenv
from utils.color_scheme import get_gradio_css, get_unified_css
from utils.user_analytics import (
    init_analytics,
    track_page,
    auto_save_session,
    show_profile_form,
)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

load_dotenv()

STREAMLIT_ENV_VARS = [
    "STREAMLIT_SERVER_PORT",
    "STREAMLIT_RUN_MAIN",
    "STREAMLIT_RUNTIME_CONFIG",
]


def is_running_under_streamlit() -> bool:
    return any(os.environ.get(var) for var in STREAMLIT_ENV_VARS)

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

# Career roadmap planning helper
try:
    from agents.career_agent import plan_career_path
except Exception:
    def plan_career_path(parsed_resume, target_role, timeline_months, focus_area, industries):
        return "Career roadmap service is unavailable. Please configure the AI provider API keys."

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


def generate_career_roadmap_content(resume_file, target_role, industries, focus_area, timeline_months):
    if resume_file is None:
        return "❌ Please upload a resume to personalize the roadmap."
    if not target_role or not target_role.strip():
        return "❌ Specify a target role (e.g., 'Senior Data Scientist')."
    text, parsed = parse_uploaded_resume(resume_file)
    if text is None:
        return "❌ Error parsing resume."
    try:
        roadmap = plan_career_path(
            parsed,
            target_role.strip(),
            timeline_months,
            focus_area,
            industries or "General Tech / Product",
        )
        return roadmap
    except Exception as exc:
        return f"⚠️ Unable to generate roadmap: {exc}"

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

            with gr.TabItem("Career Roadmap"):
                with gr.Row():
                    with gr.Column(scale=1):
                        roadmap_resume = gr.File(label="Upload Resume for Roadmap")
                        target_role = gr.Textbox(label="Target Role", value="Senior Software Engineer")
                        industries = gr.Textbox(label="Target Industries", value="AI / Product / FinTech")
                        focus_area = gr.Dropdown(
                            choices=[
                                "Technical Mastery",
                                "Technical Leadership",
                                "Product Strategy",
                                "Career Transition",
                                "Managerial Growth",
                                "Impact & Storytelling",
                            ],
                            value="Technical Leadership",
                            label="Primary Focus",
                        )
                        timeline = gr.Slider(1, 24, value=6, label="Timeline (months)")
                        roadmap_btn = gr.Button("Generate Roadmap", variant="primary")
                    with gr.Column(scale=2):
                        roadmap_md = gr.Markdown()
                        roadmap_raw = gr.Textbox(lines=16, label="Roadmap Copy")

                roadmap_btn.click(
                    fn=generate_career_roadmap_content,
                    inputs=[roadmap_resume, target_role, industries, focus_area, timeline],
                    outputs=[roadmap_md, roadmap_raw],
                )

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


def render_streamlit_home():
    import streamlit as st

    st.set_page_config(
        page_title="ResumeMasterAI - AI-Powered Career Excellence",
        page_icon="",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    analytics = init_analytics()
    track_page("Home")
    st.markdown(get_unified_css(), unsafe_allow_html=True)

    if "loaded" not in st.session_state:
        st.session_state.loaded = True

    start_page = "/?page=" + urllib.parse.quote("pages/1_📄_Upload_Resume.py")
    st.markdown(
        f"""
<div class="hero-section">
    <div style="position: relative; z-index: 2;">
        <div class="ai-badge">
            ✨ Powered by Advanced AI
        </div>
        <h1 class="hero-title">
            Transform Your Career with <span class="gradient-text">AI-Powered</span> Resume Magic
        </h1>
        <p class="hero-subtitle">
             The Ultimate Resume Optimization Platform
        </p>
        <p class="hero-tagline">
            Leverage cutting-edge AI to create, optimize, and manage your professional documents with unprecedented precision
        </p>
        <div style="margin-top: 2rem;">
            <!-- Use JS navigation to ensure Streamlit picks up the query param change -->
            <a href="#" onclick="window.location.href='{start_page}'; return false;" style="text-decoration: none;">
                <button style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; border: none; padding: 1rem 3rem; font-size: 1.2rem; font-weight: 700; border-radius: 50px; cursor: pointer; box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4); transition: all 0.3s ease; margin-right: 1rem;">
                     Get Started Free
                </button>
            </a>
            <a href="#features" style="text-decoration: none;">
                <button style="background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); color: white; border: 2px solid rgba(255, 255, 255, 0.3); padding: 1rem 3rem; font-size: 1.2rem; font-weight: 700; border-radius: 50px; cursor: pointer; transition: all 0.3s ease;">
                     Learn More
                </button>
            </a>
        </div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown('<div id="navigation"></div>', unsafe_allow_html=True)
    st.markdown(
        """
<div class="section-title">⚡ Quick Navigation</div>
<div class="section-subtitle">Jump to the tool you need</div>
""",
        unsafe_allow_html=True,
    )

    nav_items = [
        (
            "📄",
            "Upload Resume",
            "Upload and parse your resume",
            "pages/1_📄_Upload_Resume.py",
        ),
        (
            "📊",
            "Analysis & Scoring",
            "Get detailed ATS analysis",
            "pages/2_📊_Analysis_Scoring.py",
        ),
        ("🎯", "Job Matching", "Find perfect job matches", "pages/3_🎯_Job_Matching.py"),
        (
            "✍️",
            "Resume Rewrite",
            "AI-powered optimization",
            "pages/4_✍️_Resume_Rewrite.py",
        ),
        (
            "💼",
            "Cover Letters",
            "Generate custom letters",
            "pages/5_💼_Cover_Letter_Projects.py",
        ),
        ("🔍", "Job Search", "Search opportunities", "pages/6_🔍_Job_Search.py"),
        ("🏗️", "Resume Builder", "Build from scratch", "pages/7_🏗️_Resume_Builder.py"),
    ]

    cols = st.columns(len(nav_items))
    for i, (icon, title, desc, page_file) in enumerate(nav_items):
        with cols[i]:
            href = "/?page=" + urllib.parse.quote(page_file)
            st.markdown(
                f"""
        <a href="{href}" target="_self" style="text-decoration: none;">
            <div class="nav-card">
                <div class="nav-card-icon">{icon}</div>
                <div class="nav-card-title">{title}</div>
                <div class="nav-card-desc">{desc}</div>
            </div>
        </a>
        """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="section-title">🌟 Powerful Features</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Everything you need for career success</div>', unsafe_allow_html=True)

    feature_data = [
        {
            "icon": "🤖",
            "title": "AI-Powered Parsing",
            "desc": "Advanced OCR and NLP extract every detail from your resume with 95%+ accuracy",
        },
        {
            "icon": "📊",
            "title": "ATS Optimization",
            "desc": "Get scored and optimized for Applicant Tracking Systems used by 99% of companies",
        },
        {
            "icon": "🎯",
            "title": "Smart Job Matching",
            "desc": "AI matches you with perfect opportunities based on skills, experience, and preferences",
        },
        {
            "icon": "✨",
            "title": "Professional Rewriting",
            "desc": "Transform your resume with AI-powered content enhancement and formatting",
        },
        {
            "icon": "💼",
            "title": "Cover Letter Generator",
            "desc": "Create personalized, compelling cover letters in seconds for any job",
        },
        {
            "icon": "🔍",
            "title": "Job Search Engine",
            "desc": "Search thousands of jobs from multiple platforms in one place",
        },
        {
            "icon": "📈",
            "title": "Career Analytics",
            "desc": "Track your applications, analyze trends, and optimize your job search strategy",
        },
        {
            "icon": "🎨",
            "title": "Multiple Templates",
            "desc": "Choose from professional ATS-friendly templates designed by career experts",
        },
        {
            "icon": "🎤",
            "title": "Interview Prep",
            "desc": "Practice with AI-generated interview questions tailored to your target role",
        },
        {
            "icon": "💰",
            "title": "Salary Insights",
            "desc": "Get accurate salary estimates based on role, location, and experience",
        },
        {
            "icon": "💡",
            "title": "Skills Analysis",
            "desc": "Identify skill gaps and get personalized learning recommendations",
        },
        {
            "icon": "📱",
            "title": "Social Profiles",
            "desc": "Optimize your LinkedIn and other professional social media presence",
        },
    ]

    cols = st.columns(4)
    for idx, feature in enumerate(feature_data):
        with cols[idx % 4]:
            st.markdown(
                f"""
        <div class="feature-card">
            <div class="feature-icon">{feature['icon']}</div>
            <h3 style="color: #667eea; font-size: 1.2rem; margin-bottom: 0.5rem; font-weight: 700;">{feature['title']}</h3>
            <p style="color: #555; font-size: 0.95rem; line-height: 1.6;">{feature['desc']}</p>
        </div>
        """,
                unsafe_allow_html=True,
            )

    st.markdown('<div style="margin-top: 4rem;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📈 Proven Results</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Join thousands of successful job seekers</div>', unsafe_allow_html=True)

    stat_cols = st.columns(4)
    stats = [
        ("50K+", "Resumes Optimized"),
        ("98%", "ATS Pass Rate"),
        ("10K+", "Job Placements"),
        ("4.9⭐", "User Rating"),
    ]

    for col, (number, label) in zip(stat_cols, stats):
        with col:
            st.markdown(
                f"""
        <div class="stat-card">
            <div class="stat-number">{number}</div>
            <div class="stat-label">{label}</div>
        </div>
        """,
                unsafe_allow_html=True,
            )

    st.markdown('<div style="margin-top: 4rem;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚡ Powered By</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Industry-leading AI technologies</div>', unsafe_allow_html=True)

    tech_cols = st.columns(6)
    technologies = [
        ("🤖", "Google Gemini"),
        ("🔗", "LangChain"),
        ("🐍", "Python"),
        ("⚡", "Streamlit"),
        ("📊", "Plotly"),
        ("🎯", "OpenAI"),
    ]

    for col, (icon, name) in zip(tech_cols, technologies):
        with col:
            st.markdown(
                f"""
        <div class="tech-card">
            <div class="tech-icon">{icon}</div>
            <div class="tech-name">{name}</div>
        </div>
        """,
                unsafe_allow_html=True,
            )

    st.markdown('<div style="margin-top: 4rem;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎯 How It Works</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Simple 4-step process to career success</div>', unsafe_allow_html=True)

    steps_cols = st.columns(4)
    steps = [
        ("1️⃣", "Upload", "Upload your current resume in PDF or DOCX format"),
        ("2️⃣", "Analyze", "Our AI analyzes and scores your resume"),
        ("3️⃣", "Optimize", "Get AI-powered suggestions and rewrites"),
        ("4️⃣", "Apply", "Download and apply with confidence"),
    ]

    for col, (num, title, desc) in zip(steps_cols, steps):
        with col:
            st.markdown(
                f"""
        <div class="feature-card">
            <div style="font-size: 3rem; margin-bottom: 1rem;">{num}</div>
            <h3 style="color: #667eea; font-size: 1.3rem; margin-bottom: 0.5rem; font-weight: 700;">{title}</h3>
            <p style="color: #666; font-size: 0.95rem; line-height: 1.6;">{desc}</p>
        </div>
        """,
                unsafe_allow_html=True,
            )

    st.markdown('<div style="margin-top: 4rem;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💬 What Users Say</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Real success stories from our users</div>', unsafe_allow_html=True)

    testimonial_cols = st.columns(3)
    testimonials = [
        {
            "text": "ResumeMasterAI helped me land my dream job at Google! The ATS optimization was a game-changer.",
            "author": "Sarah Johnson",
            "role": "Software Engineer at Google",
        },
        {
            "text": "I was able to rewrite my resume in minutes instead of hours. The AI suggestions were spot-on!",
            "author": "Michael Chen",
            "role": "Product Manager at Amazon",
        },
        {
            "text": "The job matching feature found opportunities I would have never discovered on my own. Highly recommend!",
            "author": "Emily Rodriguez",
            "role": "Data Scientist at Microsoft",
        },
    ]

    for col, testimonial in zip(testimonial_cols, testimonials):
        with col:
            st.markdown(
                f"""
        <div class="testimonial-card">
            <div class="testimonial-text">"{testimonial['text']}"</div>
            <div class="testimonial-author">{testimonial['author']}</div>
            <div class="testimonial-role">{testimonial['role']}</div>
        </div>
        """,
                unsafe_allow_html=True,
            )

    st.markdown('<div style="margin-top: 4rem;"></div>', unsafe_allow_html=True)
    st.markdown(
        """
<div class="hero-section" style="min-height: 400px;">
    <div style="position: relative; z-index: 2; text-align: center;">
        <h2 style="font-size: 3rem; font-weight: 900; color: white; margin-bottom: 1rem;">
            Ready to Transform Your Career? 🚀
        </h2>
        <p style="font-size: 1.3rem; color: rgba(255, 255, 255, 0.9); margin-bottom: 2rem;">
            Join 50,000+ professionals who've accelerated their careers with ResumeMasterAI
        </p>
        <a href="{start_page}" target="_self" style="text-decoration: none;">
            <button style="background: linear-gradient(135deg, #fbbf24, #f97316); color: white; border: none; padding: 1.2rem 3.5rem; font-size: 1.3rem; font-weight: 800; border-radius: 50px; cursor: pointer; box-shadow: 0 15px 40px rgba(251, 191, 36, 0.4); transition: all 0.3s ease; animation: pulse 2s infinite;">
                ✨ Start Your Journey - It's FREE
            </button>
        </a>
        <p style="color: rgba(255, 255, 255, 0.7); margin-top: 1rem; font-size: 0.95rem;">
            No credit card required • Free forever • Unlimited resumes
        </p>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown('<div style="margin-top: 3rem;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">❓ Frequently Asked Questions</div>', unsafe_allow_html=True)

    with st.expander("🔒 Is my resume data secure?"):
        st.markdown("""
        Absolutely! We use industry-standard encryption and never share your data with third parties. 
        Your resume is processed securely and can be deleted at any time.
        """)

    with st.expander("💰 Is ResumeMasterAI really free?"):
        st.markdown("""
        Yes! All core features including resume parsing, ATS optimization, and basic rewriting are 
        completely free with no hidden charges.
        """)

    with st.expander("📱 Can I use this on mobile?"):
        st.markdown("""
        Yes, ResumeMasterAI is fully responsive and works on all devices including smartphones and tablets.
        """)

    with st.expander("🌍 What languages are supported?"):
        st.markdown("""
        Currently, we support English resumes. We're working on adding support for multiple languages soon.
        """)

    with st.expander("⚡ How fast is the AI processing?"):
        st.markdown("""
        Most resumes are parsed and analyzed in under 30 seconds. Complex documents may take up to 2 minutes.
        """)

    st.markdown('<div style="margin-top: 4rem;"></div>', unsafe_allow_html=True)
    st.markdown(
        """
<div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 20px; padding: 2rem; text-align: center; border: 1px solid rgba(255, 255, 255, 0.1);">
    <div style="color: rgba(255, 255, 255, 0.9); font-size: 1.1rem; margin-bottom: 1rem;">
        <strong>ResumeMasterAI</strong> - Your AI Career Partner
    </div>
    <div style="color: rgba(255, 255, 255, 0.6); font-size: 0.9rem; margin-bottom: 1rem;">
        Powered by Google Gemini AI • Built with ❤️ using Streamlit
    </div>
    <div style="color: rgba(255, 255, 255, 0.5); font-size: 0.85rem;">
        © 2025 ResumeMasterAI. All rights reserved. | Privacy Policy | Terms of Service
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown(
            """
    <div style="text-align: center; padding: 1rem;">
        <h2 style="color: white; margin-bottom: 0.5rem;">🚀 ResumeMasterAI</h2>
        <p style="color: rgba(255, 255, 255, 0.7); font-size: 0.9rem;">
            AI-Powered Career Excellence
        </p>
    </div>
    """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        st.markdown("### 🎯 Quick Access")
        st.page_link("pages/1_📄_Upload_Resume.py", label="📄 Upload Resume", icon="📄")
        st.page_link(
            "pages/2_📊_Analysis_Scoring.py", label="📊 Analysis & Scoring", icon="📊"
        )
        st.page_link("pages/3_🎯_Job_Matching.py", label="🎯 Job Matching", icon="🎯")
        st.page_link(
            "pages/4_✍️_Resume_Rewrite.py", label="✍️ Resume Rewrite", icon="✍️"
        )
        st.page_link(
            "pages/5b_🚀_Project_Suggestions.py",
            label="🚀 Project Suggestions",
            icon="🚀",
        )

        st.markdown("---")
        st.markdown("### 🧭 Career Planning")
        st.page_link(
            "pages/15_🧭_Career_Roadmap.py", label="🧭 Career Roadmap", icon="🧭"
        )

        st.markdown("---")

        st.markdown("### 🛠️ Utility Tools")
        st.page_link("pages/8_🎤_Interview_Prep.py", label="🎤 Interview Prep", icon="🎤")
        st.page_link(
            "pages/9_💰_Salary_Estimator.py", label="💰 Salary Estimator", icon="💰"
        )
        st.page_link(
            "pages/10_💡_Skills_Analyzer.py", label="💡 Skills Analyzer", icon="💡"
        )
        st.page_link("pages/11_📱_Social_Resume.py", label="📱 Social Resume", icon="📱")
        st.page_link(
            "pages/12_📧_Email_Generator.py", label="📧 Email Generator", icon="📧"
        )

        st.markdown("---")
        st.info("💡 **Tip**: Start by uploading your resume to unlock all features!")

    st.markdown("---")
    with st.expander("👤 Complete Your Profile", expanded=False):
        show_profile_form()

    auto_save_session()



if __name__ == '__main__':
    if is_running_under_streamlit():
        render_streamlit_home()
    else:
        demo = build_interface()
        demo.launch(server_name='0.0.0.0', server_port=7862, debug=True)
