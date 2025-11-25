"""
Career planning assistant service. Generates career roadmaps via multi-model LLMs.
"""

from typing import Dict
from utils.llm_utils import get_llm, generate_text


def _build_resume_context(parsed_resume: Dict) -> str:
    """Build a short summary of the resume to include in the LLM prompt."""
    if not parsed_resume:
        return "No resume data provided."

    skills = parsed_resume.get("skills", [])[:12]
    experience = parsed_resume.get("experience", [])[:6]
    education = parsed_resume.get("education", [])[:4]
    raw_text = parsed_resume.get("raw_text", "")

    context_sections = [
        f"Skills: {', '.join(skills) if skills else 'Not available'}",
        f"Key Experience Highlights: {', '.join(experience) if experience else 'Not available'}",
        f"Education: {', '.join(education) if education else 'Not available'}",
    ]

    snippet = raw_text.replace("\n", " ")[:1000]
    if snippet:
        context_sections.append(f"Resume Snippet Excerpt: {snippet}")

    return "\n".join(context_sections)


def generate_career_roadmap(
    parsed_resume: Dict,
    target_role: str,
    timeline_months: int,
    focus_area: str,
    industries: str,
) -> str:
    """Generate a textual career roadmap using the configured LLM."""
    llm = get_llm()
    if not llm.is_available():
        raise RuntimeError("No LLM provider configured. Set an API key to enable career planning.")

    resume_context = _build_resume_context(parsed_resume)
    industries_txt = industries or "General Tech and Product"

    prompt = f"""
You are a pragmatic career coach who helps ambitious individuals reach their next milestone.

Resume Context:
{resume_context}

Goal:
The candidate wants to reach the role of {target_role} within {timeline_months} month(s).
Focus Area: {focus_area}
Preferred Industries/Companies: {industries_txt}

Produce a clear roadmap with the following sections:
1. Goal Vision (short statement)
2. Strengths to spotlight (based on the resume)
3. Key skills/projects/certifications to build or refresh
4. Networking & visibility moves (LinkedIn, communities, referrals)
5. Interview prep focus (e.g., STAR stories, technical drills, mock conversations)
6. Four-week milestone plan covering the timeline that leads to the goal
7. Risk mitigation (what to watch out for)

Return the roadmap using markdown headings and bullet lists so it can be displayed directly in the UI.
"""

    response = generate_text(prompt, temperature=0.7, max_tokens=1600)
    return response.strip()
