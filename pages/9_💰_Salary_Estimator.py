"""
Salary Estimator - Data-Driven Salary Insights
Estimate salary based on role, experience, location, and skills.
"""

import streamlit as st
import sys
import uuid
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.salary_estimator import SalaryEstimator
from utils.color_scheme import get_unified_css
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Salary Estimator - ResumeMasterAI", page_icon="💰", layout="wide"
)

# Apply unified CSS
st.markdown(get_unified_css(), unsafe_allow_html=True)

# Custom CSS
st.markdown(
    """
<style>
    .salary-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .salary-number {
        font-size: 3rem;
        font-weight: 900;
        margin: 1rem 0;
    }
    
    .insight-box {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .range-box {
        background: #f0f9ff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #3b82f6;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Header
st.markdown("# 💰 Salary Estimator")
st.markdown("### Data-driven salary insights based on role, experience, and skills")

# Initialize session state
if "salary_estimate" not in st.session_state:
    st.session_state.salary_estimate = None

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Input Details")

    # Job Information
    st.subheader("📋 Job Details")
    job_title = st.text_input(
        "Job Title",
        placeholder="e.g., Senior Software Engineer",
        help="Enter the job title/role",
    )

    industry = st.selectbox(
        "Industry",
        [
            "Technology",
            "Finance",
            "Healthcare",
            "Consulting",
            "Marketing",
            "Sales",
            "Engineering",
            "Education",
            "Manufacturing",
            "Other",
        ],
    )

    # Experience
    st.subheader("👔 Experience")
    years_experience = st.slider(
        "Years of Experience", min_value=0, max_value=30, value=5, step=1
    )

    experience_level = st.select_slider(
        "Experience Level",
        options=[
            "Entry",
            "Junior",
            "Mid-Level",
            "Senior",
            "Lead",
            "Principal",
            "Executive",
        ],
        value="Mid-Level",
    )

    # Location
    st.subheader("📍 Location")
    country = st.selectbox(
        "Country",
        [
            "United States",
            "Canada",
            "United Kingdom",
            "Germany",
            "Australia",
            "India",
            "Singapore",
            "Other",
        ],
    )

    city = st.text_input("City (Optional)", placeholder="e.g., San Francisco")

    # Education
    st.subheader("🎓 Education")
    education_level = st.selectbox(
        "Highest Degree",
        ["High School", "Associate", "Bachelor's", "Master's", "PhD", "Other"],
    )

    # Company Size
    st.subheader("🏢 Company")
    company_size = st.selectbox(
        "Company Size",
        [
            "Startup (1-50)",
            "Small (51-200)",
            "Medium (201-1000)",
            "Large (1001-5000)",
            "Enterprise (5000+)",
        ],
    )

# Main Content
tab1, tab2, tab3 = st.tabs(["💰 Estimate", "📊 Analysis", "📈 Trends"])

with tab1:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 🛠️ Skills & Expertise")

        technical_skills = st.text_area(
            "Technical Skills (comma-separated)",
            placeholder="Python, AWS, Docker, Kubernetes, React...",
            height=100,
        )

        soft_skills = st.text_area(
            "Soft Skills (comma-separated)",
            placeholder="Leadership, Communication, Problem-solving...",
            height=80,
        )

        certifications = st.text_input(
            "Certifications (comma-separated)",
            placeholder="AWS Certified, PMP, CISSP...",
        )

    with col2:
        st.markdown("### 💡 Additional Factors")

        remote_work = st.checkbox("Remote Work", value=False)
        management = st.checkbox("Management Role", value=False)
        specialized = st.checkbox("Specialized Domain", value=False)

        st.info("""
        **Salary Factors:**
        
        ✓ Experience level
        
        ✓ Location & COL
        
        ✓ Skills & expertise
        
        ✓ Industry demand
        
        ✓ Company size
        """)

    # Generate Estimate Button
    if st.button(
        "💰 Calculate Salary Estimate", type="primary", use_container_width=True, key="calculate_salary_btn"
    ):
        if not job_title:
            st.error("❌ Please enter a job title")
        else:
            with st.spinner("🤖 Analyzing salary data..."):
                try:
                    estimator = SalaryEstimator()

                    # Prepare input data
                    input_data = {
                        "job_title": job_title,
                        "industry": industry,
                        "years_experience": years_experience,
                        "experience_level": experience_level,
                        "country": country,
                        "city": city,
                        "education": education_level,
                        "company_size": company_size,
                        "technical_skills": [
                            s.strip() for s in technical_skills.split(",") if s.strip()
                        ],
                        "soft_skills": [
                            s.strip() for s in soft_skills.split(",") if s.strip()
                        ],
                        "certifications": [
                            c.strip() for c in certifications.split(",") if c.strip()
                        ],
                        "remote_work": remote_work,
                        "management": management,
                        "specialized": specialized,
                    }

                    # Get estimate
                    estimate = estimator.estimate_salary(input_data)
                    st.session_state.salary_estimate = estimate

                    st.success("✅ Salary estimate calculated!")

                except Exception as e:
                    st.error(f"❌ Error calculating estimate: {str(e)}")

    # Display Results
    if st.session_state.salary_estimate:
        st.markdown("---")
        st.markdown("## 💵 Your Salary Estimate")

        estimate = st.session_state.salary_estimate

        # Main salary display
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                f"""
            <div class="range-box">
                <h4>Minimum</h4>
                <h2 style="color: #f59e0b;">${estimate.get("min", 0):,}</h2>
                <p>25th percentile</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                f"""
            <div class="salary-card">
                <h4>Average Estimate</h4>
                <div class="salary-number">${estimate.get("average", 0):,}</div>
                <p>Based on your profile</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                f"""
            <div class="range-box">
                <h4>Maximum</h4>
                <h2 style="color: #10b981;">${estimate.get("max", 0):,}</h2>
                <p>75th percentile</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        # Confidence & Factors
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📊 Confidence Level")
            confidence = estimate.get("confidence", 75)
            st.progress(confidence / 100)
            st.markdown(
                f"**{confidence}%** - Based on {estimate.get('data_points', 'available')} data points"
            )

        with col2:
            st.markdown("### 🔍 Key Factors")
            factors = estimate.get("factors", {})
            for factor, impact in factors.items():
                st.markdown(f"- **{factor}:** {impact}")

with tab2:
    st.markdown("## 📊 Salary Analysis")

    if st.session_state.salary_estimate:
        estimate = st.session_state.salary_estimate

        col1, col2 = st.columns(2)

        with col1:
            # Salary Distribution
            st.markdown("### 📈 Salary Distribution")

            fig = go.Figure()
            fig.add_trace(
                go.Box(
                    y=[
                        estimate.get("min", 0),
                        estimate.get("average", 0),
                        estimate.get("max", 0),
                    ],
                    name="Salary Range",
                    marker_color="#667eea",
                )
            )
            fig.update_layout(
                title="Your Salary Range",
                yaxis_title="Annual Salary ($)",
                showlegend=False,
                height=400,
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Skills Impact
            st.markdown("### 💡 Skills Impact")

            skills_value = estimate.get("skills_breakdown", {})
            if skills_value:
                fig = px.bar(
                    x=list(skills_value.values()),
                    y=list(skills_value.keys()),
                    orientation="h",
                    title="Skill Value Contribution",
                    color=list(skills_value.values()),
                    color_continuous_scale="Viridis",
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Add technical skills to see their value impact")

        # Comparison
        st.markdown("### 🔄 Market Comparison")

        col1, col2, col3 = st.columns(3)

        with col1:
            market_avg = estimate.get("market_average", estimate.get("average", 0))
            diff = estimate.get("average", 0) - market_avg
            st.metric(
                "vs Market Average", f"${estimate.get('average', 0):,}", f"${diff:+,}"
            )

        with col2:
            industry_avg = estimate.get("industry_average", estimate.get("average", 0))
            diff = estimate.get("average", 0) - industry_avg
            st.metric(
                "vs Industry Average", f"${estimate.get('average', 0):,}", f"${diff:+,}"
            )

        with col3:
            location_avg = estimate.get("location_average", estimate.get("average", 0))
            diff = estimate.get("average", 0) - location_avg
            st.metric(
                "vs Location Average", f"${estimate.get('average', 0):,}", f"${diff:+,}"
            )

    else:
        st.info("👈 Calculate a salary estimate first to see the analysis")

with tab3:
    st.markdown("## 📈 Salary Trends")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Experience vs Salary")

        # Sample trend data
        experience_years = list(range(0, 21, 2))
        base_salary = 60000
        salaries = [
            base_salary + (year * 5000) + (year**1.5 * 2000)
            for year in experience_years
        ]

        fig = px.line(
            x=experience_years,
            y=salaries,
            title="Typical Salary Growth by Experience",
            labels={"x": "Years of Experience", "y": "Annual Salary ($)"},
            markers=True,
        )
        fig.update_traces(line_color="#667eea", marker_color="#764ba2")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🌍 Location Comparison")

        locations = ["San Francisco", "New York", "Austin", "Seattle", "Remote"]
        salaries_by_loc = [180000, 170000, 140000, 165000, 150000]

        fig = px.bar(
            x=locations,
            y=salaries_by_loc,
            title="Average Salaries by Location",
            labels={"x": "Location", "y": "Annual Salary ($)"},
            color=salaries_by_loc,
            color_continuous_scale="Viridis",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 💼 Industry Insights")

    st.info("""
    **Key Trends:**
    
    📈 **Tech Industry:** 15-20% average annual growth for in-demand skills
    
    🌐 **Remote Work:** 10-15% salary premium for fully remote positions
    
    🎓 **Advanced Degrees:** 20-30% higher salaries on average
    
    🏆 **Certifications:** 5-15% salary boost depending on relevance
    
    🌟 **Specialized Skills:** AI/ML, Cloud, and Cybersecurity command premiums
    """)

# Resources
st.markdown("---")
st.markdown("## 📚 Salary Negotiation Tips")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🎯 Research
    - Know your market value
    - Research company budgets
    - Consider total comp
    - Factor in benefits
    - Understand equity
    """)

with col2:
    st.markdown("""
    ### 💬 Negotiation
    - State your range
    - Justify with data
    - Be confident
    - Consider timing
    - Get it in writing
    """)

with col3:
    st.markdown("""
    ### ✅ Best Practices
    - Don't share current salary
    - Focus on value added
    - Be flexible on details
    - Know your walk-away
    - Stay professional
    """)

# Footer
st.markdown("---")
st.markdown(
    """
<div style='text-align: center; color: #6b7280;'>
    <p>💡 <strong>Disclaimer:</strong> Estimates are based on industry data and should be used as guidance only.</p>
</div>
""",
    unsafe_allow_html=True,
)
