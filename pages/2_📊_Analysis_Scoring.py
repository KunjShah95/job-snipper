"""
Resume Analysis & Scoring Page
Comprehensive scoring and analysis with professional visualizations.
"""

import streamlit as st
import os
import sys
import uuid

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.color_scheme import get_unified_css
from utils.scoring_utils import compute_subscores, combine_scores, explain_score
from utils.workflow_visual import create_score_visualization
from agents.scoring_agent import score_resume
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Analysis & Scoring - ResumeMasterAI", page_icon="📊", layout="wide"
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
if "score" not in st.session_state:
    st.session_state.score = None
if "subscores" not in st.session_state:
    st.session_state.subscores = None
if "explanations" not in st.session_state:
    st.session_state.explanations = None

# Header
st.markdown("# 📊 Resume Analysis & Scoring")

# Check if resume is parsed
if not st.session_state.parsed:
    st.warning("⚠️ Please upload and parse a resume first!")
    if st.button("📄 Go to Upload Page", key="go_to_upload_analysis"):
        st.switch_page("pages/1_📄_Upload_Resume.py")
    st.stop()

st.markdown(
    """
<div class="custom-card">
    <p style="font-size: 1.1rem; color: #4F5D75;">
        Our AI analyzes your resume across multiple dimensions to provide comprehensive insights 
        and actionable recommendations for improvement.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

# Analyze button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🔍 Analyze Resume", use_container_width=True, type="primary", key="analyze_resume_btn"):
        with st.spinner("🤖 AI is analyzing your resume..."):
            try:
                # Basic scoring
                basic_score = score_resume(st.session_state.parsed).get("score", 0)

                # Detailed subscores
                subs = compute_subscores(st.session_state.parsed)
                combined = combine_scores(subs)
                explanations = explain_score(st.session_state.parsed, subs)

                # Store in session state
                st.session_state.score = combined["overall"]
                st.session_state.subscores = subs
                st.session_state.explanations = explanations

                st.success("✅ Analysis complete!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error during analysis: {e}")

# Display results if available
if st.session_state.score is not None:
    # Overall Score Section
    st.markdown("## 🎯 Overall Score")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        score_html = create_score_badge(st.session_state.score)
        st.markdown(
            f"""
        <div style="text-align: center; padding: 2rem; background: white; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            {score_html}
            <p style="margin-top: 1rem; color: #4F5D75; font-size: 1rem;">
                Your resume is performing {"excellently" if st.session_state.score >= 80 else "well" if st.session_state.score >= 60 else "below expectations"}.
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Score Breakdown Visualization
    st.markdown("## 📈 Detailed Score Breakdown")

    if st.session_state.subscores:
        # Create visualization
        try:
            viz_path = create_score_visualization(
                st.session_state.subscores,
                st.session_state.score,
                out_filename=f"score_viz_{int(__import__('time').time())}",
            )
            st.image(viz_path, use_container_width=True)
        except Exception as e:
            st.error(f"Could not generate visualization: {e}")

            # Fallback to table display
            import pandas as pd

            df = pd.DataFrame(
                list(st.session_state.subscores.items()), columns=["Category", "Score"]
            )
            df = df.sort_values("Score", ascending=False)
            st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Category Scores in Cards
    st.markdown("## 🎨 Score by Category")

    if st.session_state.subscores:
        # Create columns for score cards
        categories = list(st.session_state.subscores.items())

        # Split into rows of 3
        for i in range(0, len(categories), 3):
            cols = st.columns(3)
            for j, (category, score) in enumerate(categories[i : i + 3]):
                with cols[j]:
                    # Determine color based on score
                    if score >= 80:
                        color = "#06A77D"
                        emoji = "✅"
                    elif score >= 60:
                        color = "#F18F01"
                        emoji = "⚠️"
                    else:
                        color = "#C73E1D"
                        emoji = "❌"

                    st.markdown(
                        f"""
                    <div class="stat-box" style="border-top: 4px solid {color};">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{emoji}</div>
                        <div class="stat-number" style="color: {color};">{score:.0f}</div>
                        <div class="stat-label">{category.title()}</div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Feedback and Recommendations
    st.markdown("## 💡 AI Insights & Recommendations")

    if st.session_state.explanations:
        # Group by priority
        critical = []
        improvements = []
        strengths = []

        for explanation in st.session_state.explanations:
            if any(
                word in explanation.lower()
                for word in ["critical", "missing", "lack", "insufficient"]
            ):
                critical.append(explanation)
            elif any(
                word in explanation.lower()
                for word in ["improve", "consider", "enhance", "add"]
            ):
                improvements.append(explanation)
            else:
                strengths.append(explanation)

        # Critical Issues
        if critical:
            with st.expander(
                "🚨 Critical Issues (Immediate Attention Required)", expanded=True
            ):
                for item in critical:
                    st.markdown(
                        f"""
                    <div style="background: #fee; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 4px solid #C73E1D;">
                        {item}
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

        # Improvements
        if improvements:
            with st.expander("⚠️ Areas for Improvement", expanded=True):
                for item in improvements:
                    st.markdown(
                        f"""
                    <div style="background: #fff8e6; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 4px solid #F18F01;">
                        {item}
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

        # Strengths
        if strengths:
            with st.expander("✅ Strengths & Good Practices", expanded=True):
                for item in strengths:
                    st.markdown(
                        f"""
                    <div style="background: #e6ffe6; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 4px solid #06A77D;">
                        {item}
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

    # Action Items Summary
    st.markdown("## 📋 Quick Action Items")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        <div class="custom-card">
            <h3>🎯 Top Priorities</h3>
            <ol style="line-height: 2;">
                <li>Add quantifiable achievements to experience</li>
                <li>Include relevant industry keywords</li>
                <li>Optimize formatting and structure</li>
                <li>Ensure contact information is complete</li>
            </ol>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="custom-card">
            <h3>💡 Pro Tips</h3>
            <ul style="line-height: 2;">
                <li>Use action verbs to describe experience</li>
                <li>Tailor content to target job descriptions</li>
                <li>Keep resume to 1-2 pages maximum</li>
                <li>Proofread for grammar and spelling</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Next Steps
    st.markdown("---")
    st.markdown("### ✨ Ready for the next step?")

    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            "🎯 Match with Job Description", use_container_width=True, type="primary", key=f"match_job_description_{uuid.uuid4()}"
        ):
            st.switch_page("pages/3_🎯_Job_Matching.py")
    with col2:
        if st.button("✍️ Rewrite Resume", use_container_width=True, key="rewrite_resume_analysis"):
            st.switch_page("pages/4_✍️_Resume_Rewrite.py")

else:
    st.info("👆 Click 'Analyze Resume' to see your comprehensive score and insights.")

    # Preview what analysis includes
    st.markdown("### 📋 What Our Analysis Includes")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **📊 Multi-dimensional Scoring:**
        - Skills assessment
        - Experience evaluation
        - Education review
        - Format and structure analysis
        - Keyword optimization
        """)

    with col2:
        st.markdown("""
        **💡 Actionable Insights:**
        - Detailed feedback for each category
        - Priority-ranked recommendations
        - Industry best practices
        - Competitive benchmarking
        - Improvement roadmap
        """)

# Progress indicator
st.markdown("---")
st.markdown(
    """
<div style="text-align: center; padding: 1rem;">
    <p style="color: #4F5D75; font-size: 0.9rem;">
        <strong>Step 2 of 6:</strong> Analysis & Scoring
    </p>
    <div style="background: #E5E5E5; height: 6px; border-radius: 3px; overflow: hidden; max-width: 600px; margin: 0.5rem auto;">
        <div style="background: linear-gradient(90deg, #2E86AB 0%, #06A77D 100%); height: 100%; width: 33.33%;"></div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)
