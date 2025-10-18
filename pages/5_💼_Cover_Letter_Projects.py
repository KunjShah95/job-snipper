"""
Cover Letter Generation & Project Suggestions Page
Generate tailored cover letters and get project recommendations.
"""

import streamlit as st
import os
import sys
import uuid
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.color_scheme import get_unified_css
from agents.coverletter_agent import generate_cover_letter
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Cover Letter - ResumeMasterAI", page_icon="💼", layout="wide"
)

# Apply unified color scheme
st.markdown(get_unified_css(), unsafe_allow_html=True)

# Initialize session state
if "parsed" not in st.session_state:
    st.session_state.parsed = None
if "cover_letter" not in st.session_state:
    st.session_state.cover_letter = None
if "projects" not in st.session_state:
    st.session_state.projects = None
if "jd_for_cl" not in st.session_state:
    st.session_state.jd_for_cl = ""

# Header
st.markdown("# 💼 Cover Letter Generator")

# Check if resume is parsed
if not st.session_state.parsed:
    st.warning("⚠️ Please upload and parse a resume first!")
    if st.button("📄 Go to Upload Page", key="go_to_upload_cover"):
        st.switch_page("pages/1_📄_Upload_Resume.py")
    st.stop()

# Cover Letter Generator
with st.container():
    st.markdown(
        """
    <div class="custom-card">
        <p style="font-size: 1.1rem; color: #4F5D75;">
            Create a personalized cover letter tailored to a specific job. 
            Our AI analyzes your resume and the job description to craft a compelling narrative.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Job details input
    st.markdown("## 📋 Job Details")

    col1, col2 = st.columns(2)

    with col1:
        company_name = st.text_input(
            "Company Name",
            placeholder="e.g., Google, Microsoft, Amazon",
            help="The company you're applying to",
        )

    with col2:
        job_title = st.text_input(
            "Job Title",
            placeholder="e.g., Senior Software Engineer",
            help="The position you're applying for",
        )

    job_description = st.text_area(
        "Job Description (Optional but recommended)",
        value=st.session_state.jd_for_cl,
        height=200,
        placeholder="Paste the job description here for a more tailored cover letter...",
        help="Including the job description helps generate a more targeted cover letter",
    )

    st.session_state.jd_for_cl = job_description

    # Additional preferences
    with st.expander("⚙️ Advanced Options"):
        col1, col2 = st.columns(2)

        with col1:
            tone = st.selectbox(
                "Tone",
                ["Professional", "Enthusiastic", "Formal", "Creative"],
                help="The tone of your cover letter",
            )

        with col2:
            length = st.selectbox(
                "Length",
                [
                    "Concise (3 paragraphs)",
                    "Standard (4 paragraphs)",
                    "Detailed (5+ paragraphs)",
                ],
                help="Preferred cover letter length",
            )

        highlight_skills = st.text_input(
            "Skills to Highlight (comma-separated)",
            placeholder="e.g., Python, Leadership, Machine Learning",
            help="Specific skills you want to emphasize",
        )

    # Generate button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        can_generate = bool(company_name and job_title)
        if st.button(
            "✨ Generate Cover Letter",
            use_container_width=True,
            type="primary",
            disabled=not can_generate,
            key="generate_cover_letter_btn",
        ):
            with st.spinner("🤖 AI is crafting your cover letter..."):
                try:
                    # Build context
                    context = {
                        "company": company_name,
                        "position": job_title,
                        "job_description": job_description,
                        "tone": tone.lower(),
                        "highlight_skills": highlight_skills.split(",")
                        if highlight_skills
                        else [],
                    }

                    cover_letter = generate_cover_letter(
                        st.session_state.parsed, context
                    )
                    st.session_state.cover_letter = cover_letter
                    st.success("✅ Cover letter generated!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error generating cover letter: {e}")

    if not can_generate:
        st.info(
            "👆 Please provide at least the company name and job title to generate a cover letter"
        )

    # Display cover letter if generated
    if st.session_state.cover_letter:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("## 📄 Your Cover Letter")

        # Editable text area
        edited_cl = st.text_area(
            "Cover Letter (Editable)",
            value=st.session_state.cover_letter,
            height=500,
            help="Feel free to edit the cover letter as needed",
            label_visibility="collapsed",
        )

        st.session_state.cover_letter = edited_cl

        # Download options
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.download_button(
                label="📄 Download TXT",
                data=edited_cl,
                file_name=f"cover_letter_{company_name.replace(' ', '_')}_{timestamp}.txt",
                mime="text/plain",
                use_container_width=True,
            )

        with col2:
            st.download_button(
                label="📝 Download MD",
                data=edited_cl,
                file_name=f"cover_letter_{company_name.replace(' ', '_')}_{timestamp}.md",
                mime="text/markdown",
                use_container_width=True,
            )

        with col3:
            if st.button("📋 Copy Text", use_container_width=True, key="copy_text_btn"):
                st.code(edited_cl, language=None)
                st.info("👆 Select and copy the text above")

        with col4:
            if st.button("🔄 Regenerate", use_container_width=True, key="regenerate_cover_btn"):
                st.session_state.cover_letter = None
                st.rerun()

        # Tips
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            """
        <div class="custom-card" style="background: #E8F5E9; border-left-color: #06A77D;">
            <h4>💡 Cover Letter Tips</h4>
            <ul style="line-height: 2; color: #4F5D75;">
                <li>Personalize the opening paragraph with why you're interested in this specific company</li>
                <li>Use specific examples from your experience that match job requirements</li>
                <li>Show enthusiasm and cultural fit</li>
                <li>Keep it concise - hiring managers spend ~30 seconds per cover letter</li>
                <li>Proofread carefully for typos and grammar errors</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Link to Project Suggestions page
    st.markdown("---")
    st.markdown(
        """
    <div class="custom-card">
        <p style="font-size: 1.05rem; color: #4F5D75;">
            Project suggestions are now available on a separate page to keep features focused.
            <strong>If you'd like to get project ideas</strong>, visit the Projects page below.
        </p>
        <div style="text-align:center; margin-top: 1rem;">
            <a class="button-link" href="/?page=pages/5b_🚀_Project_Suggestions.py">� Go to Project Suggestions</a>
        </div>
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
        <strong>Step 5 of 6:</strong> Cover Letter & Project Suggestions
    </p>
    <div style="background: #E5E5E5; height: 6px; border-radius: 3px; overflow: hidden; max-width: 600px; margin: 0.5rem auto;">
        <div style="background: linear-gradient(90deg, #2E86AB 0%, #06A77D 100%); height: 100%; width: 83.33%;"></div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)
