"""
Simple test page to debug resume parsing
"""
import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.file_utils import save_uploaded_file, detect_file_type
from agents.parser_agent import parse_resume

st.set_page_config(page_title="Parse Test", page_icon="🔧", layout="wide")

st.title("🔧 Resume Parsing Debug Test")
st.markdown("This is a simplified test page to debug the parsing button.")

# Initialize session state
if "parsed" not in st.session_state:
    st.session_state.parsed = None
if "file_path" not in st.session_state:
    st.session_state.file_path = None
if "file_type" not in st.session_state:
    st.session_state.file_type = None

st.markdown("### Step 1: Upload File")
uploaded_file = st.file_uploader("Choose resume", type=["pdf", "docx", "txt"])

if uploaded_file:
    st.success(f"✅ File uploaded: {uploaded_file.name}")
    
    # Save file
    if st.session_state.file_path is None or st.session_state.file_path.split('/')[-1] != uploaded_file.name:
        with st.spinner("Saving..."):
            saved_path = save_uploaded_file(uploaded_file)
            mime, simple_type = detect_file_type(saved_path)
            st.session_state.file_path = saved_path
            st.session_state.file_type = simple_type
            st.info(f"Saved to: {saved_path}")
            st.info(f"Type: {simple_type}")

st.markdown("### Step 2: Parse")
st.markdown(f"**File path in session:** {st.session_state.file_path}")
st.markdown(f"**File type in session:** {st.session_state.file_type}")

if st.session_state.file_path:
    if st.button("🔍 Parse Resume Now", type="primary", key="parse_btn"):
        st.markdown("**Button clicked!** ✅")
        with st.spinner("Parsing..."):
            try:
                st.info(f"Calling parse_resume({st.session_state.file_path}, {st.session_state.file_type})")
                parsed = parse_resume(st.session_state.file_path, st.session_state.file_type)
                st.session_state.parsed = parsed
                st.success("✅ Parse complete!")
                st.json(parsed)
            except Exception as e:
                st.error(f"❌ Error: {e}")
                import traceback
                st.code(traceback.format_exc())
else:
    st.warning("⚠️ No file uploaded yet")

st.markdown("### Step 3: View Results")
if st.session_state.parsed:
    st.success("✅ Parsed data exists in session!")
    with st.expander("View parsed data"):
        st.json(st.session_state.parsed)
else:
    st.info("No parsed data yet")

st.markdown("---")
st.markdown("### Debug Info")
st.markdown("**Session State:**")
st.write({
    "parsed_exists": st.session_state.parsed is not None,
    "file_path": st.session_state.file_path,
    "file_type": st.session_state.file_type
})
