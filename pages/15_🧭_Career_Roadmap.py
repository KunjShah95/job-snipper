"""Career roadmap planner page."""

import os
import sys
import uuid
from datetime import datetime

import streamlit as st

# Allow imports from root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from utils.color_scheme import get_unified_css
from agents.career_agent import plan_career_path

load_dotenv()

st.set_page_config(page_title="Career Roadmap - ResumeMasterAI", page_icon="🧭", layout="wide")
st.markdown(get_unified_css(), unsafe_allow_html=True)

if "parsed" not in st.session_state or not st.session_state.parsed:
    st.warning("⚠️ Please upload and parse a resume on the Upload page before building a roadmap.")
    if st.button("📄 Go to Upload Resume", key=f"redirect_upload_{uuid.uuid4()}"):
        st.switch_page("pages/1_📄_Upload_Resume.py")
    st.stop()

resume = st.session_state.parsed
skills = resume.get("skills", [])
experiences = resume.get("experience", [])
education = resume.get("education", [])
snapshot = resume.get("raw_text", "")[:400]

if "career_roadmap_text" not in st.session_state:
    st.session_state.career_roadmap_text = None

if "career_goal_inputs" not in st.session_state:
    st.session_state.career_goal_inputs = {
        "target_role": "Senior Software Engineer",
        "industries": "AI / Product / FinTech",
        "focus_area": "Technical Leadership",
        "timeline": 6,
    }

st.markdown("# 🧭 Career Roadmap Planner")
st.markdown(
    "<div class=\"custom-card\"><p style=\"color:#4F5D75;\">Plot a practical plan that translates your resume into the role you care about most. This roadmap organizes skills, projects, networking, and interview prep into a timeline you can share or revisit.</p></div>",
    unsafe_allow_html=True,
)

col1, col2, col3, col4 = st.columns([1.25, 1, 1, 1])
col1.metric("Skills Captured", len(skills))
col2.metric("Experience Highlights", len(experiences))
col3.metric("Education Entries", len(education))
col4.metric("Timeline Target (months)", st.session_state.career_goal_inputs["timeline"])

with st.expander("Résumé Snapshot", expanded=False):
    st.markdown(f"**Top skills:** {', '.join(skills[:8]) or 'Not yet extracted.'}")
    st.markdown(f"**Experience cues:** {', '.join(experiences[:5]) or 'Not yet extracted.'}")
    st.markdown(f"**Excerpt:** {snapshot or 'No resume text available.'}")

with st.form("career_roadmap_form"):
    target_role = st.text_input(
        "Target Job Title",
        value=st.session_state.career_goal_inputs["target_role"],
        help="Name the role you are actively pursuing or aiming for next.",
    )
    industries = st.text_input(
        "Target Industries/Companies",
        value=st.session_state.career_goal_inputs["industries"],
        help="List industries, company types, or internal teams you want to align with.",
    )

    focus_options = [
        "Technical Mastery",
        "Technical Leadership",
        "Product Strategy",
        "Career Transition",
        "Managerial Growth",
        "Impact & Storytelling",
    ]
    default_focus_index = (
        focus_options.index(st.session_state.career_goal_inputs["focus_area"])
        if st.session_state.career_goal_inputs["focus_area"] in focus_options
        else 0
    )
    focus_area = st.selectbox(
        "Primary Focus",
        focus_options,
        index=default_focus_index,
        help="How should the roadmap prioritize your effort?",
    )

    timeline_months = st.slider(
        "Timeline (months)",
        min_value=1,
        max_value=24,
        value=st.session_state.career_goal_inputs["timeline"],
        help="How many months do you have to reach the stated goal?",
    )

    submitted = st.form_submit_button("🧠 Generate Roadmap")

    if submitted:
        if not target_role.strip():
            st.warning("Please specify the target job title before generating a roadmap.")
        else:
            st.session_state.career_goal_inputs = {
                "target_role": target_role,
                "industries": industries,
                "focus_area": focus_area,
                "timeline": timeline_months,
            }
            with st.spinner("Mapping your career story into the roadmap..."):
                roadmap_text = plan_career_path(
                    resume,
                    target_role,
                    timeline_months,
                    focus_area,
                    industries,
                )
            st.session_state.career_roadmap_text = roadmap_text

if st.session_state.career_roadmap_text:
    st.markdown("---")
    st.markdown("## 📘 Generated Roadmap")
    st.markdown(
        st.session_state.career_roadmap_text,
        unsafe_allow_html=False,
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    download_data = st.session_state.career_roadmap_text.encode("utf-8")

    col_dl1, col_dl2 = st.columns([1, 1])
    with col_dl1:
        st.download_button(
            label="📥 Download Roadmap",
            data=download_data,
            file_name=f"career_roadmap_{timestamp}.md",
            mime="text/markdown",
            use_container_width=True,
        )
    with col_dl2:
        if st.button("🔄 Regenerate Roadmap", key=f"regen_career_{uuid.uuid4()}"):
            st.session_state.career_roadmap_text = None
            st.experimental_rerun()

else:
    st.info("Share a target title plus focus area to visualize a tactical roadmap using generative AI.")

st.markdown("---")
st.markdown(
    "<div style=\"text-align:center; font-size:0.9rem; color:#4F5D75;\">Step 6 of 7: Career Roadmap · Reinforce the narrative you created earlier with clear next steps.</div>",
    unsafe_allow_html=True,
)
