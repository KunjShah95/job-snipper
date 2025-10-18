"""
Job Matching & Skill Gap Analysis Page
Match your resume with job descriptions and identify skill gaps.
"""

import streamlit as st
import os
import sys
import uuid

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.color_scheme import get_unified_css
from utils.workflow_visual import create_skill_match_visualization
from agents.matcher_agent import match_resume
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Job Matching - ResumeMasterAI", page_icon="🎯", layout="wide"
)

# Apply unified color scheme
st.markdown(get_unified_css(), unsafe_allow_html=True)


# Helper function for score badge
def create_score_badge(score):
    """Create a styled score badge."""
    color = "#22c55e" if score >= 80 else "#f59e0b" if score >= 60 else "#ef4444"
    return f"""
    <div style="display: inline-block; padding: 1rem 2rem; background: linear-gradient(135deg, {color}, {color}dd); 
         border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
        <span style="font-size: 3rem; font-weight: 700; color: white;">{score}</span>
        <span style="font-size: 1.5rem; color: white; opacity: 0.9;">/100</span>
    </div>
    """


# Initialize session state
if "parsed" not in st.session_state:
    st.session_state.parsed = None
if "match_info" not in st.session_state:
    st.session_state.match_info = None
if "jd_text" not in st.session_state:
    st.session_state.jd_text = ""

# Header
st.markdown("# 🎯 Job Matching & Skill Gap Analysis")

# Check if resume is parsed
if not st.session_state.parsed:
    st.warning("⚠️ Please upload and parse a resume first!")
    if st.button("📄 Go to Upload Page", key="go_to_upload_matching"):
        st.switch_page("pages/1_📄_Upload_Resume.py")
    st.stop()

st.markdown(
    """
<div class="custom-card">
    <p style="font-size: 1.1rem; color: #4F5D75;">
        Paste a job description below to analyze how well your resume matches the requirements. 
        Our AI will identify matched skills, missing skills, and provide recommendations to improve your match score.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

# Job Description Input
st.markdown("## 📝 Job Description")

jd_text = st.text_area(
    "Paste the complete job description here",
    value=st.session_state.jd_text,
    height=300,
    placeholder="""Example:
    
We are seeking a Senior Software Engineer with:
- 5+ years of experience in Python and JavaScript
- Strong knowledge of React, Node.js, and MongoDB
- Experience with cloud platforms (AWS, Azure)
- Excellent problem-solving skills
- Bachelor's degree in Computer Science or related field
    
Responsibilities include developing scalable web applications, collaborating with cross-functional teams, and mentoring junior developers...""",
)

st.session_state.jd_text = jd_text

# Match button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    match_button = st.button(
        "🔍 Analyze Job Match",
        use_container_width=True,
        type="primary",
        disabled=not jd_text.strip(),
        key=f"analyze_job_match_{uuid.uuid4()}",
    )

if match_button and jd_text.strip():
    with st.spinner("🤖 AI is analyzing the match..."):
        try:
            match_info = match_resume(st.session_state.parsed, jd_text)
            st.session_state.match_info = match_info
            st.success("✅ Analysis complete!")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error during matching: {e}")

# Display results if available
if st.session_state.match_info and jd_text.strip():
    match_info = st.session_state.match_info
    match_score = match_info.get("match_score", 0)
    matched_skills = match_info.get("matched_skills", [])
    missing_skills = match_info.get("missing_skills", [])

    # Overall Match Score
    st.markdown("## 🎯 Match Score")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        score_html = create_score_badge(match_score)

        # Interpretation
        if match_score >= 80:
            interpretation = "Excellent match! You meet most requirements."
            icon = "🌟"
        elif match_score >= 60:
            interpretation = "Good match! Consider addressing skill gaps."
            icon = "✅"
        else:
            interpretation = "Moderate match. Significant skill development needed."
            icon = "⚠️"

        st.markdown(
            f"""
        <div style="text-align: center; padding: 2rem; background: white; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            <div style="font-size: 3rem; margin-bottom: 1rem;">{icon}</div>
            {score_html}
            <p style="margin-top: 1rem; color: #4F5D75; font-size: 1.1rem;">
                {interpretation}
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Visualization
    st.markdown("## 📊 Visual Analysis")

    try:
        viz_path = create_skill_match_visualization(
            matched_skills,
            missing_skills,
            match_score,
            out_filename=f"match_viz_{int(__import__('time').time())}",
        )
        st.image(viz_path, use_container_width=True)
    except Exception as e:
        st.warning(f"Could not generate visualization: {e}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Skills Analysis
    st.markdown("## 📋 Detailed Skills Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
        <div class="custom-card" style="border-left-color: #06A77D; background: #e6ffe6;">
            <h3 style="color: #06A77D;">✅ Matched Skills ({len(matched_skills)})</h3>
            <p style="color: #4F5D75; margin-bottom: 1rem;">Skills you already have that match the job requirements:</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if matched_skills:
            # Display as styled pills
            skills_html = " ".join(
                [
                    f'<span style="display: inline-block; background: linear-gradient(135deg, #06A77D 0%, #04D98B 100%); color: white; padding: 0.4rem 0.9rem; margin: 0.3rem; border-radius: 15px; font-size: 0.9rem; font-weight: 500;">✓ {skill}</span>'
                    for skill in matched_skills[:50]
                ]
            )
            st.markdown(skills_html, unsafe_allow_html=True)

            if len(matched_skills) > 50:
                with st.expander(
                    f"Show {len(matched_skills) - 50} more matched skills"
                ):
                    more_skills = " ".join(
                        [
                            f'<span style="display: inline-block; background: linear-gradient(135deg, #06A77D 0%, #04D98B 100%); color: white; padding: 0.4rem 0.9rem; margin: 0.3rem; border-radius: 15px; font-size: 0.9rem; font-weight: 500;">✓ {skill}</span>'
                            for skill in matched_skills[50:]
                        ]
                    )
                    st.markdown(more_skills, unsafe_allow_html=True)
        else:
            st.info("No matching skills identified. Consider updating your resume.")

    with col2:
        st.markdown(
            f"""
        <div class="custom-card" style="border-left-color: #C73E1D; background: #fee;">
            <h3 style="color: #C73E1D;">❌ Missing Skills ({len(missing_skills)})</h3>
            <p style="color: #4F5D75; margin-bottom: 1rem;">Skills mentioned in the job description that you should develop:</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if missing_skills:
            # Display as styled pills
            skills_html = " ".join(
                [
                    f'<span style="display: inline-block; background: linear-gradient(135deg, #C73E1D 0%, #E85D4A 100%); color: white; padding: 0.4rem 0.9rem; margin: 0.3rem; border-radius: 15px; font-size: 0.9rem; font-weight: 500;">! {skill}</span>'
                    for skill in missing_skills[:50]
                ]
            )
            st.markdown(skills_html, unsafe_allow_html=True)

            if len(missing_skills) > 50:
                with st.expander(
                    f"Show {len(missing_skills) - 50} more missing skills"
                ):
                    more_skills = " ".join(
                        [
                            f'<span style="display: inline-block; background: linear-gradient(135deg, #C73E1D 0%, #E85D4A 100%); color: white; padding: 0.4rem 0.9rem; margin: 0.3rem; border-radius: 15px; font-size: 0.9rem; font-weight: 500;">! {skill}</span>'
                            for skill in missing_skills[50:]
                        ]
                    )
                    st.markdown(more_skills, unsafe_allow_html=True)
        else:
            st.success("Great! No major skill gaps identified.")

    st.markdown("<br>", unsafe_allow_html=True)

    # Recommendations
    st.markdown("## 💡 Recommendations")

    if missing_skills:
        priority_skills = missing_skills[:5]

        st.markdown(
            """
        <div class="custom-card">
            <h3>🎯 Priority Skills to Develop</h3>
            <p style="color: #4F5D75; margin-bottom: 1rem;">
                Focus on these high-impact skills to significantly improve your match score:
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        for i, skill in enumerate(priority_skills, 1):
            st.markdown(
                f"""
            <div style="background: white; padding: 1.2rem; border-radius: 10px; margin-bottom: 0.8rem; box-shadow: 0 2px 4px rgba(0,0,0,0.08); border-left: 4px solid #2E86AB;">
                <div style="display: flex; align-items: center;">
                    <div style="background: linear-gradient(135deg, #2E86AB 0%, #06A77D 100%); color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 1rem;">
                        {i}
                    </div>
                    <div style="flex: 1;">
                        <strong style="font-size: 1.1rem; color: #2D3142;">{skill}</strong>
                    </div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        # Action buttons
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button(
                "📚 Get Project Suggestions", use_container_width=True, type="primary", key=f"get_project_suggestions_{uuid.uuid4()}"
            ):
                st.switch_page("pages/5_💼_Cover_Letter_Projects.py")
        with col2:
            if st.button("✍️ Optimize Resume", use_container_width=True, key="optimize_resume_matching"):
                st.switch_page("pages/4_✍️_Resume_Rewrite.py")

    # Statistics
    st.markdown("## 📈 Match Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
        <div class="stat-box">
            <div class="stat-number">{match_score:.0f}%</div>
            <div class="stat-label">Overall Match</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
        <div class="stat-box">
            <div class="stat-number">{len(matched_skills)}</div>
            <div class="stat-label">Matched Skills</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
        <div class="stat-box">
            <div class="stat-number">{len(missing_skills)}</div>
            <div class="stat-label">Skills to Develop</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col4:
        coverage = (
            (len(matched_skills) / (len(matched_skills) + len(missing_skills)) * 100)
            if (len(matched_skills) + len(missing_skills)) > 0
            else 0
        )
        st.markdown(
            f"""
        <div class="stat-box">
            <div class="stat-number">{coverage:.0f}%</div>
            <div class="stat-label">Skill Coverage</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

else:
    st.info(
        "👆 Paste a job description above and click 'Analyze Job Match' to see detailed matching results."
    )

    # Tips for best results
    st.markdown("### 💡 Tips for Best Results")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        <div class="custom-card">
            <h3>📋 What to Include</h3>
            <ul style="line-height: 2;">
                <li>Complete job title and company</li>
                <li>Required and preferred qualifications</li>
                <li>Technical skills and tools</li>
                <li>Years of experience required</li>
                <li>Education requirements</li>
                <li>Job responsibilities</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="custom-card">
            <h3>🎯 Best Practices</h3>
            <ul style="line-height: 2;">
                <li>Copy the entire job posting</li>
                <li>Include both required and nice-to-have skills</li>
                <li>Don't edit or summarize the description</li>
                <li>Make sure formatting is preserved</li>
                <li>Include company culture information</li>
                <li>Add any specific certifications mentioned</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

# Progress indicator
st.markdown("---")
st.markdown(
    """
<div style="text-align: center; padding: 1rem;">
    <p style="color: #4F5D75; font-size: 0.9rem;">
        <strong>Step 3 of 6:</strong> Job Matching & Skill Gap Analysis
    </p>
    <div style="background: #E5E5E5; height: 6px; border-radius: 3px; overflow: hidden; max-width: 600px; margin: 0.5rem auto;">
        <div style="background: linear-gradient(90deg, #2E86AB 0%, #06A77D 100%); height: 100%; width: 50%;"></div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)
