"""
Resume Upload & Parsing Page
Upload your resume and parse it into structured data.
"""

import streamlit as st
import json
import uuid
from utils.file_utils import save_uploaded_file, detect_file_type
from agents.parser_agent import parse_resume
from agents.project_agent import suggest_projects
from utils.user_analytics import init_analytics, show_feedback_widget, auto_save_session
from utils.color_scheme import get_unified_css

st.set_page_config(page_title="Upload Resume - ResumeMasterAI", page_icon="📄", layout="wide")

st.markdown(get_unified_css(), unsafe_allow_html=True)
st.markdown("# 📄 Upload Resume")

# initialize analytics instance
analytics = init_analytics()

# Initialize session state defaults
if "parsed" not in st.session_state:
    st.session_state.parsed = None
if "file_path" not in st.session_state:
    st.session_state.file_path = None
if "file_type" not in st.session_state:
    st.session_state.file_type = None
if "projects" not in st.session_state:
    st.session_state.projects = None

col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader(
        "Choose your resume file",
        type=["pdf", "docx", "txt"],
        help="Supported formats: PDF, DOCX, TXT",
        key="upload_resume_main",
    )

    if uploaded_file:
        # Track resume upload
        file_size = len(uploaded_file.getvalue()) if hasattr(uploaded_file, "getvalue") else 0
        file_type = uploaded_file.name.split('.')[-1] if hasattr(uploaded_file, 'name') else 'unknown'
        analytics.track_resume_upload(file_type, file_size)
        analytics.track_feature_usage('resume_upload', {'file_type': file_type})

        with st.spinner("Saving file..."):
            saved_path = save_uploaded_file(uploaded_file)
            mime, simple_type = detect_file_type(saved_path)
            st.session_state.file_path = saved_path
            st.session_state.file_type = simple_type

        st.success(f"✅ File uploaded successfully: `{uploaded_file.name}`")
        st.info(f"📋 File type detected: **{simple_type.upper()}**")

        # Parse button - use stable key based on file path
        if st.button("🔍 Parse Resume", use_container_width=True, type="primary", key="parse_resume_btn"):
            with st.spinner("🤖 AI is parsing your resume... This may take a moment."):
                try:
                    parsed = parse_resume(st.session_state.file_path, st.session_state.file_type)
                    st.session_state.parsed = parsed
                    st.success("✅ Resume parsed successfully!")
                    
                    # Auto-redirect to Analysis & Scoring page
                    st.info("🔄 Redirecting to Analysis & Scoring...")
                    import time
                    time.sleep(1)
                    st.switch_page("pages/2_📊_Analysis_Scoring.py")
                    
                except Exception as e:
                    st.error(f"❌ Error parsing resume: {e}")
                    import traceback
                    st.error(f"Details: {traceback.format_exc()}")

with col2:
    st.markdown("## 📌 Tips")
    st.markdown(
        "- Use a clear, well-formatted resume\n- Avoid heavy graphics for best parsing\n- Include keywords relevant to your target role"
    )

if st.session_state.parsed:
    st.markdown("---")
    st.markdown("## 👤 Parsed Summary")

    parsed = st.session_state.parsed

    # Show manifest/diagnostics if present
    manifest = parsed.get("_manifest")
    if manifest:
        with st.expander("Parsing manifest / diagnostics"):
            st.json(manifest)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"**Name:** {parsed.get('name', 'Not detected')}")
        st.markdown(f"**Email:** {parsed.get('email', 'Not detected')}")
    with col_b:
        st.markdown(f"**Phone:** {parsed.get('phone', 'Not detected')}")
        st.markdown(f"**Location:** {parsed.get('location', 'Not detected')}")

    # Skills preview
    st.markdown("### 💼 Skills")
    skills = parsed.get("skills", [])
    if skills:
        st.write(", ".join(skills[:50]))
    else:
        st.warning("No skills detected")

    # Raw text and download
    st.markdown("---")
    json_data = json.dumps(parsed, indent=2)
    st.download_button(
        label="📥 Download Parsed Data (JSON)",
        data=json_data,
        file_name="parsed_resume.json",
        mime="application/json",
        key="download_parsed_json",
    )

    # Quick link to Project Suggestions
    st.markdown("---")
    if st.button("🚀 Suggest Projects", use_container_width=True, type="primary", key="suggest_projects_btn"):
        # Save session data before navigation
        auto_save_session()
        st.query_params["page"] = "5b_🚀_Project_Suggestions"# Feedback and autosave
st.markdown("---")
show_feedback_widget("Upload Resume")
auto_save_session()
