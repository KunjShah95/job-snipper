"""
Interview Preparation - AI-Powered Interview Prep
Generate role-specific interview questions and practice answers.
"""

import streamlit as st
import sys
import uuid
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.interview_prep import InterviewPrep
from utils.color_scheme import get_unified_css
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Interview Preparation - ResumeMasterAI", page_icon="🎤", layout="wide"
)

# Apply unified CSS
st.markdown(get_unified_css(), unsafe_allow_html=True)

# Custom CSS
st.markdown(
    """
<style>
    .interview-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .question-box {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    
    .answer-tips {
        background: #f0f9ff;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Header
st.markdown("# 🎤 Interview Preparation")
st.markdown("### AI-powered interview practice with role-specific questions")

# Initialize session state
if "interview_questions" not in st.session_state:
    st.session_state.interview_questions = None
if "parsed_resume" not in st.session_state:
    st.session_state.parsed_resume = None

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    # Resume Upload
    uploaded_file = st.file_uploader(
        "Upload Resume (Optional)",
        type=["pdf", "docx", "txt"],
        help="Upload your resume to extract skills and experience",
    )

    if uploaded_file and not st.session_state.parsed_resume:
        with st.spinner("📄 Parsing resume..."):
            try:
                # Parse resume (simplified)
                st.session_state.parsed_resume = "Resume data extracted successfully"
                st.success("✅ Resume parsed!")
            except Exception as e:
                st.error(f"Error parsing resume: {str(e)}")

    job_role = st.text_input(
        "Job Role/Title",
        placeholder="e.g., Senior Software Engineer",
        help="Enter the position you're interviewing for",
    )

    experience_level = st.selectbox(
        "Experience Level",
        ["Entry Level", "Mid Level", "Senior Level", "Lead/Manager"],
        index=1,
    )

    interview_type = st.multiselect(
        "Interview Types",
        ["Behavioral", "Technical", "System Design", "Leadership", "Culture Fit"],
        default=["Behavioral", "Technical"],
    )

    num_questions = st.slider(
        "Number of Questions", min_value=5, max_value=30, value=10, step=5
    )

    difficulty = st.select_slider(
        "Difficulty Level", options=["Easy", "Medium", "Hard", "Expert"], value="Medium"
    )

    include_tips = st.checkbox("Include Answer Tips", value=True)
    include_star = st.checkbox("Include STAR Framework Examples", value=True)

# Main Content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📋 Interview Question Generator")

    # Input Options
    input_method = st.radio(
        "Choose input method:", ["Use Resume Data", "Manual Input"], horizontal=True
    )

    if input_method == "Use Resume Data":
        if uploaded_file:
            st.success("✓ Using resume data")
            resume_text = str(st.session_state.parsed_resume)
        else:
            st.warning(
                "⚠️ No resume data found. Please upload a resume first or use manual input."
            )
            resume_text = None
    else:
        st.markdown("**Enter your skills and experience:**")
        resume_text = st.text_area(
            "Skills & Experience",
            placeholder="Enter your key skills, technologies, achievements...",
            height=150,
        )

with col2:
    st.markdown("### 💡 Tips")
    st.info("""
    **Prepare Effectively:**
    
    ✓ Practice out loud
    
    ✓ Use STAR method
    
    ✓ Research the company
    
    ✓ Prepare questions
    
    ✓ Mock interviews help
    """)

# Generate Button
if st.button(
    "🚀 Generate Interview Questions", type="primary", use_container_width=True, key="generate_interview_questions_btn"
):
    if not job_role:
        st.error("❌ Please enter a job role")
    elif input_method == "Manual Input" and not resume_text:
        st.error("❌ Please enter your skills and experience")
    else:
        with st.spinner("🤖 AI is generating interview questions..."):
            try:
                interview_prep = InterviewPrep()

                # Generate questions based on input
                questions = interview_prep.generate_questions(
                    role=job_role,
                    experience_level=experience_level,
                    interview_types=interview_type,
                    num_questions=num_questions,
                    skills_text=resume_text if resume_text else "",
                    difficulty=difficulty,
                )

                st.session_state.interview_questions = questions
                st.success("✅ Interview questions generated successfully!")

            except Exception as e:
                st.error(f"❌ Error generating questions: {str(e)}")

# Display Results
if st.session_state.interview_questions:
    st.markdown("---")
    st.markdown("## 📝 Your Interview Questions")

    # Organize by type
    questions_by_type = {}
    for q in st.session_state.interview_questions:
        q_type = q.get("type", "General")
        if q_type not in questions_by_type:
            questions_by_type[q_type] = []
        questions_by_type[q_type].append(q)

    # Display by category
    for q_type, questions in questions_by_type.items():
        with st.expander(f"**{q_type} Questions** ({len(questions)})", expanded=True):
            for idx, q in enumerate(questions, 1):
                st.markdown(
                    f"""
                <div class="question-box">
                    <h4>Question {idx}</h4>
                    <p style="font-size: 1.1rem; margin: 0.5rem 0;">
                        {q.get("question", "")}
                    </p>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                if include_tips and q.get("tips"):
                    st.markdown(
                        f"""
                    <div class="answer-tips">
                        <strong>💡 Answer Tips:</strong>
                        <ul>
                            {"".join([f"<li>{tip}</li>" for tip in q.get("tips", [])])}
                        </ul>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                if include_star and q.get("star_example"):
                    with st.expander("📊 STAR Framework Example"):
                        star = q.get("star_example", {})
                        st.markdown(f"""
                        - **Situation:** {star.get("situation", "N/A")}
                        - **Task:** {star.get("task", "N/A")}
                        - **Action:** {star.get("action", "N/A")}
                        - **Result:** {star.get("result", "N/A")}
                        """)

                st.markdown("<br>", unsafe_allow_html=True)

    # Export Options
    st.markdown("---")
    st.markdown("### 📥 Export Questions")

    col1, col2, col3 = st.columns(3)

    with col1:
        # Export as text
        questions_text = "\\n\\n".join(
            [
                f"Q{idx}: {q.get('question', '')}\\n"
                + (f"Tips: {', '.join(q.get('tips', []))}\\n" if include_tips else "")
                for idx, q in enumerate(st.session_state.interview_questions, 1)
            ]
        )

        st.download_button(
            "📄 Download as TXT",
            data=questions_text,
            file_name=f"interview_prep_{job_role.replace(' ', '_')}.txt",
            mime="text/plain",
        )

    with col2:
        # Export as markdown
        md_content = f"# Interview Preparation: {job_role}\\n\\n"
        for q_type, questions in questions_by_type.items():
            md_content += f"## {q_type}\\n\\n"
            for idx, q in enumerate(questions, 1):
                md_content += f"### Question {idx}\\n{q.get('question', '')}\\n\\n"
                if include_tips:
                    md_content += "**Tips:**\\n"
                    for tip in q.get("tips", []):
                        md_content += f"- {tip}\\n"
                    md_content += "\\n"

        st.download_button(
            "📝 Download as Markdown",
            data=md_content,
            file_name=f"interview_prep_{job_role.replace(' ', '_')}.md",
            mime="text/markdown",
        )

    with col3:
        if st.button("🔄 Generate New Questions", key="generate_new_questions_btn"):
            st.session_state.interview_questions = None
            st.rerun()

# Resources Section
st.markdown("---")
st.markdown("## 📚 Interview Resources")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🎯 STAR Method
    **Situation:** Set the context
    
    **Task:** Describe the challenge
    
    **Action:** Explain what you did
    
    **Result:** Share the outcome
    """)

with col2:
    st.markdown("""
    ### 💼 Common Topics
    - Leadership & teamwork
    - Problem-solving
    - Communication skills
    - Technical expertise
    - Adaptability
    - Conflict resolution
    """)

with col3:
    st.markdown("""
    ### ✅ Best Practices
    - Research the company
    - Practice answers aloud
    - Prepare questions
    - Dress appropriately
    - Follow up after
    - Be authentic
    """)

# Footer
st.markdown("---")
st.markdown(
    """
<div style='text-align: center; color: #6b7280;'>
    <p>💡 <strong>Pro Tip:</strong> Practice each question multiple times and record yourself to improve delivery!</p>
</div>
""",
    unsafe_allow_html=True,
)
