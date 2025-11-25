"""
Job Search & Recommendations Page
Search for relevant jobs based on your resume and preferences.
"""

import streamlit as st
import os
import sys
import uuid
import pandas as pd
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.color_scheme import get_unified_css
from agents.jobsearch_agent import search_jobs
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Job Search - ResumeMasterAI", page_icon="🔍", layout="wide"
)

# Apply unified color scheme
st.markdown(get_unified_css(), unsafe_allow_html=True)

# Initialize session state
if "parsed" not in st.session_state:
    st.session_state.parsed = None
if "job_results" not in st.session_state:
    st.session_state.job_results = None
if "search_params" not in st.session_state:
    st.session_state.search_params = {}

# Header
st.markdown("# 🔍 Job Search & Recommendations")

# Check if resume is parsed
if not st.session_state.parsed:
    st.warning("⚠️ Please upload and parse a resume first!")
    if st.button("📄 Go to Upload Page", key="go_to_upload_job"):
        st.switch_page("pages/1_📄_Upload_Resume.py")
    st.stop()

st.markdown(
    """
<div class="custom-card">
    <p style="font-size: 1.1rem; color: #4F5D75;">
        Discover job opportunities that match your skills and experience. 
        Our AI analyzes your resume to recommend the most relevant positions.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

# Search parameters
st.markdown("## 🔧 Search Criteria")

col1, col2, col3 = st.columns(3)

with col1:
    job_title = st.text_input(
        "Job Title / Role",
        value=st.session_state.search_params.get("job_title", ""),
        placeholder="e.g., Software Engineer, Data Scientist",
        help="The type of role you're looking for",
    )

with col2:
    location = st.text_input(
        "Location",
        value=st.session_state.search_params.get("location", ""),
        placeholder="e.g., San Francisco, Remote, New York",
        help="Preferred job location",
    )

with col3:
    experience_level = st.selectbox(
        "Experience Level",
        ["Any", "Entry Level", "Mid Level", "Senior Level", "Executive"],
        index=0,
        help="Your experience level",
    )

# Advanced filters
with st.expander("🔍 Advanced Filters"):
    col1, col2 = st.columns(2)

    with col1:
        job_type = st.multiselect(
            "Job Type",
            ["Full-time", "Part-time", "Contract", "Internship", "Temporary"],
            default=["Full-time"],
            help="Type of employment",
        )

        salary_min = st.number_input(
            "Minimum Salary ($K/year)",
            min_value=0,
            max_value=500,
            value=0,
            step=10,
            help="Minimum annual salary in thousands",
        )

    with col2:
        remote_options = st.multiselect(
            "Remote Preference",
            ["On-site", "Hybrid", "Remote"],
            default=["On-site", "Hybrid", "Remote"],
            help="Work location preference",
        )

        num_results = st.slider(
            "Number of Results",
            min_value=5,
            max_value=50,
            value=20,
            step=5,
            help="How many job listings to fetch",
        )

# Store search params
st.session_state.search_params = {
    "job_title": job_title,
    "location": location,
    "experience_level": experience_level,
    "job_type": job_type,
    "remote_options": remote_options,
    "salary_min": salary_min,
    "num_results": num_results,
}

# Search button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    can_search = bool(job_title or location)
    if st.button(
        "🔍 Search Jobs",
        use_container_width=True,
        type="primary",
        disabled=not can_search,
        key="search_jobs_btn",
    ):
        with st.spinner("🤖 AI is searching for relevant jobs..."):
            try:
                search_query = {
                    "keywords": job_title,
                    "location": location,
                    "experience_level": experience_level
                    if experience_level != "Any"
                    else None,
                    "job_type": job_type,
                    "remote": remote_options,
                    "min_salary": salary_min * 1000 if salary_min > 0 else None,
                    "limit": num_results,
                }

                jobs = search_jobs(st.session_state.parsed, search_query)
                st.session_state.job_results = jobs
                st.success(f"✅ Found {len(jobs) if jobs else 0} job opportunities!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error searching for jobs: {e}")

if not can_search:
    st.info("👆 Enter at least a job title or location to search for jobs")

st.markdown("<br>", unsafe_allow_html=True)

# Display job results
if st.session_state.job_results:
    jobs = (
        st.session_state.job_results
        if isinstance(st.session_state.job_results, list)
        else []
    )

    if not jobs:
        st.warning(
            "No jobs found matching your criteria. Try adjusting your search parameters."
        )
    else:
        # Statistics
        st.markdown("## 📊 Search Results")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                f"""
            <div class="stat-box">
                <div class="stat-number">{len(jobs)}</div>
                <div class="stat-label">Jobs Found</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col2:
            # Count remote jobs
            remote_count = sum(
                1 for job in jobs if isinstance(job, dict) and job.get("remote", False)
            )
            st.markdown(
                f"""
            <div class="stat-box">
                <div class="stat-number">{remote_count}</div>
                <div class="stat-label">Remote Jobs</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col3:
            # Average match score
            match_scores = [
                job.get("match_score", 0)
                for job in jobs
                if isinstance(job, dict) and "match_score" in job
            ]
            avg_match = sum(match_scores) / len(match_scores) if match_scores else 0
            st.markdown(
                f"""
            <div class="stat-box">
                <div class="stat-number">{avg_match:.0f}%</div>
                <div class="stat-label">Avg Match Score</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col4:
            # Count jobs posted within last 7 days
            recent_count = sum(
                1
                for job in jobs
                if isinstance(job, dict) and job.get("days_ago", 999) <= 7
            )
            st.markdown(
                f"""
            <div class="stat-box">
                <div class="stat-number">{recent_count}</div>
                <div class="stat-label">New (7 days)</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Filter and sort options
        st.markdown("### 🎛️ Filter & Sort")

        col1, col2, col3 = st.columns(3)

        with col1:
            sort_by = st.selectbox(
                "Sort By",
                [
                    "Match Score (High to Low)",
                    "Date Posted (Newest)",
                    "Salary (High to Low)",
                    "Company Name (A-Z)",
                ],
                index=0,
            )

        with col2:
            filter_remote = st.selectbox(
                "Filter by Type",
                ["All", "Remote Only", "Hybrid Only", "On-site Only"],
                index=0,
            )

        with col3:
            min_match = st.slider(
                "Min Match Score (%)", min_value=0, max_value=100, value=0, step=5
            )

        # Apply filters and sorting
        filtered_jobs = jobs.copy()

        # Filter by remote preference
        if filter_remote != "All":
            if filter_remote == "Remote Only":
                filtered_jobs = [
                    j
                    for j in filtered_jobs
                    if isinstance(j, dict) and j.get("remote", False)
                ]
            elif filter_remote == "Hybrid Only":
                filtered_jobs = [
                    j
                    for j in filtered_jobs
                    if isinstance(j, dict) and j.get("hybrid", False)
                ]
            elif filter_remote == "On-site Only":
                filtered_jobs = [
                    j
                    for j in filtered_jobs
                    if isinstance(j, dict)
                    and not j.get("remote", False)
                    and not j.get("hybrid", False)
                ]

        # Filter by match score
        filtered_jobs = [
            j
            for j in filtered_jobs
            if isinstance(j, dict) and j.get("match_score", 0) >= min_match
        ]

        # Sort
        if sort_by == "Match Score (High to Low)":
            filtered_jobs.sort(
                key=lambda x: x.get("match_score", 0) if isinstance(x, dict) else 0,
                reverse=True,
            )
        elif sort_by == "Date Posted (Newest)":
            filtered_jobs.sort(
                key=lambda x: x.get("days_ago", 999) if isinstance(x, dict) else 999
            )
        elif sort_by == "Salary (High to Low)":
            filtered_jobs.sort(
                key=lambda x: x.get("salary", 0) if isinstance(x, dict) else 0,
                reverse=True,
            )
        elif sort_by == "Company Name (A-Z)":
            filtered_jobs.sort(
                key=lambda x: x.get("company", "") if isinstance(x, dict) else ""
            )

        st.markdown(f"**Showing {len(filtered_jobs)} of {len(jobs)} jobs**")
        st.markdown("<br>", unsafe_allow_html=True)

        # Display jobs
        st.markdown("## 💼 Job Listings")

        for idx, job in enumerate(filtered_jobs, 1):
            if not isinstance(job, dict):
                continue

            title = job.get("title", "Job Title Not Available")
            company = job.get("company", "Company Not Listed")
            location_str = job.get("location", "Location Not Specified")
            match_score = job.get("match_score", 0)
            salary = job.get("salary", "Not specified")
            days_ago = job.get("days_ago", None)
            description = job.get("description", "No description available")
            url = job.get("url", "#")
            remote = job.get("remote", False)
            hybrid = job.get("hybrid", False)

            # Match score badge color
            if match_score >= 80:
                badge_color = "#06A77D"
                badge_text = "Excellent Match"
            elif match_score >= 60:
                badge_color = "#F18F01"
                badge_text = "Good Match"
            else:
                badge_color = "#C73E1D"
                badge_text = "Fair Match"

            # Work type badge
            if remote:
                work_badge = '<span style="background: #06A77D; color: white; padding: 0.25rem 0.6rem; border-radius: 10px; font-size: 0.8rem; margin-left: 0.5rem;">🏠 Remote</span>'
            elif hybrid:
                work_badge = '<span style="background: #2E86AB; color: white; padding: 0.25rem 0.6rem; border-radius: 10px; font-size: 0.8rem; margin-left: 0.5rem;">🔄 Hybrid</span>'
            else:
                work_badge = '<span style="background: #4F5D75; color: white; padding: 0.25rem 0.6rem; border-radius: 10px; font-size: 0.8rem; margin-left: 0.5rem;">🏢 On-site</span>'

            # Date posted
            if days_ago is not None:
                if days_ago == 0:
                    date_text = "Posted today"
                elif days_ago == 1:
                    date_text = "Posted yesterday"
                else:
                    date_text = f"Posted {days_ago} days ago"
            else:
                date_text = "Date not available"

            st.markdown(
                f"""
            <div class="custom-card" style="background: white; box-shadow: 0 4px 12px rgba(0,0,0,0.1); position: relative;">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
                    <div style="flex: 1;">
                        <h3 style="color: #2D3142; margin: 0 0 0.5rem 0;">{title}</h3>
                        <p style="color: #4F5D75; font-size: 1.1rem; margin: 0;">
                            <strong>{company}</strong> • {location_str}
                        </p>
                    </div>
                    <div style="text-align: right;">
                        <span style="background: {badge_color}; color: white; padding: 0.4rem 0.9rem; border-radius: 12px; font-size: 0.9rem; font-weight: 600;">
                            {match_score}% Match
                        </span>
                    </div>
                </div>
                <div style="margin: 0.5rem 0;">
                    {work_badge}
                    <span style="color: #999; font-size: 0.85rem; margin-left: 0.5rem;">📅 {date_text}</span>
                    <span style="color: #2E86AB; font-size: 0.9rem; margin-left: 0.5rem; font-weight: 600;">💰 {salary}</span>
                </div>
                <p style="color: #4F5D75; line-height: 1.6; margin: 1rem 0;">
                    {description[:300]}{"..." if len(description) > 300 else ""}
                </p>
                <a href="{url}" target="_blank" style="display: inline-block; background: linear-gradient(135deg, #2E86AB 0%, #06A77D 100%); color: white; padding: 0.6rem 1.5rem; border-radius: 8px; text-decoration: none; font-weight: 600; margin-top: 0.5rem;">
                    View Job Details →
                </a>
            </div>
            <br>
            """,
                unsafe_allow_html=True,
            )

        # Export options
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("## 💾 Export Results")

        col1, col2, col3 = st.columns(3)

        with col1:
            # CSV export
            if filtered_jobs:
                df_data = []
                for job in filtered_jobs:
                    if isinstance(job, dict):
                        df_data.append(
                            {
                                "Title": job.get("title", ""),
                                "Company": job.get("company", ""),
                                "Location": job.get("location", ""),
                                "Match Score": job.get("match_score", 0),
                                "Salary": job.get("salary", ""),
                                "Remote": "Yes" if job.get("remote", False) else "No",
                                "URL": job.get("url", ""),
                            }
                        )

                if df_data:
                    df = pd.DataFrame(df_data)
                    csv = df.to_csv(index=False)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                    st.download_button(
                        label="📊 Download CSV",
                        data=csv,
                        file_name=f"job_search_results_{timestamp}.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )

        with col2:
            if st.button("🔄 New Search", use_container_width=True, key="new_search_btn"):
                st.session_state.job_results = None
                st.rerun()

        with col3:
            if st.button("🏠 Back to Home", use_container_width=True, key="back_to_home_btn"):
                st.switch_page("app.py")

else:
    # Tips section
    st.markdown("### 💡 Job Search Tips")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        <div class="custom-card">
            <h4>🎯 Effective Search Strategies</h4>
            <ul style="line-height: 2;">
                <li>Use specific job titles for better matches</li>
                <li>Try variations (e.g., "Software Engineer" vs "Developer")</li>
                <li>Consider remote opportunities to expand options</li>
                <li>Set realistic salary expectations based on market</li>
                <li>Focus on roles matching 70%+ of your skills</li>
                <li>Apply to jobs posted within last 7 days</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="custom-card">
            <h4>📈 Improving Your Chances</h4>
            <ul style="line-height: 2;">
                <li>Tailor your resume for each application</li>
                <li>Write personalized cover letters</li>
                <li>Highlight matching skills prominently</li>
                <li>Apply within 24-48 hours of posting</li>
                <li>Follow up after 1-2 weeks</li>
                <li>Network with employees at target companies</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Popular job boards
    st.markdown("### 🌐 Popular Job Boards")

    st.markdown(
        """
    <div class="custom-card">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
            <div>
                <strong>General:</strong><br>
                • LinkedIn<br>
                • Indeed<br>
                • Glassdoor<br>
                • ZipRecruiter
            </div>
            <div>
                <strong>Tech-Specific:</strong><br>
                • AngelList (Startups)<br>
                • Stack Overflow Jobs<br>
                • GitHub Jobs<br>
                • Dice
            </div>
            <div>
                <strong>Remote-Focused:</strong><br>
                • Remote.co<br>
                • We Work Remotely<br>
                • FlexJobs<br>
                • Remote OK
            </div>
            <div>
                <strong>Specialized:</strong><br>
                • Hired (Tech)<br>
                • Dribbble (Design)<br>
                • Behance (Creative)<br>
                • Kaggle (Data Science)
            </div>
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
        <strong>Step 6 of 6:</strong> Job Search & Recommendations - Complete! 🎉
    </p>
    <div style="background: #E5E5E5; height: 6px; border-radius: 3px; overflow: hidden; max-width: 600px; margin: 0.5rem auto;">
        <div style="background: linear-gradient(90deg, #2E86AB 0%, #06A77D 100%); height: 100%; width: 100%;"></div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# Congratulations message
if st.session_state.job_results:
    st.markdown(
        """
    <div style="background: linear-gradient(135deg, #E3F2FD 0%, #E8F5E9 100%); padding: 2rem; border-radius: 15px; text-align: center; margin-top: 2rem; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
        <h2 style="color: #2D3142; margin-bottom: 1rem;">🎉 Congratulations!</h2>
        <p style="font-size: 1.2rem; color: #4F5D75; margin-bottom: 1.5rem;">
            You've completed the entire ResumeMasterAI workflow! You now have:
        </p>
        <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
            <div style="text-align: center;">
                <div style="font-size: 2rem;">✅</div>
                <div style="color: #4F5D75;">Parsed Resume</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem;">📊</div>
                <div style="color: #4F5D75;">Scoring Analysis</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem;">🎯</div>
                <div style="color: #4F5D75;">Job Matches</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem;">✍️</div>
                <div style="color: #4F5D75;">Optimized Resume</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem;">💼</div>
                <div style="color: #4F5D75;">Cover Letters</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem;">🔍</div>
                <div style="color: #4F5D75;">Job Opportunities</div>
            </div>
        </div>
        <p style="margin-top: 1.5rem; color: #4F5D75; font-size: 1.1rem;">
            Good luck with your job search! 🚀
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )
