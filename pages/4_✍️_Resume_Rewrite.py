"""
Ultimate Resume Rewrite Page
Comprehensive resume optimization with all advanced features.
"""

import streamlit as st
import sys
import uuid
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from services.resume_parser import parse_resume_to_json
from services.resume_rewriter import ResumeRewriter
from utils.job_matcher import JobMatcher
from utils.ats_scanner import ATSScanner
from utils.version_manager import VersionManager
from utils.interview_prep import InterviewPrep
from utils.skills_analyzer import SkillsAnalyzer
from utils.email_generator import EmailGenerator
from utils.resume_grader import ResumeGrader
from utils.social_resume import SocialResumeGenerator
from utils.salary_estimator import SalaryEstimator


st.set_page_config(page_title="Ultimate Resume Rewrite", page_icon="🚀", layout="wide")

st.title("🚀 Ultimate Resume Rewrite & Career Optimizer")
st.markdown(
    "**Comprehensive toolkit for resume optimization, career advancement, and job search success**"
)

# Initialize session state
if "resume_text" not in st.session_state:
    st.session_state.resume_text = None
if "parsed_resume" not in st.session_state:
    st.session_state.parsed_resume = None
if "versions" not in st.session_state:
    st.session_state.versions = {}

# Sidebar for file upload
with st.sidebar:
    st.header("📤 Upload Resume")
    uploaded_file = st.file_uploader(
        "Choose your resume",
        type=["pdf", "docx", "txt"],
        help="Upload your current resume to get started",
    )

    if uploaded_file:
        with st.spinner("Parsing resume..."):
            if uploaded_file.type == "application/pdf":
                from services.pdf_parser import parse_pdf

                st.session_state.resume_text = parse_pdf(uploaded_file)
            elif (
                uploaded_file.type
                == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ):
                from services.docx_parser import parse_docx

                st.session_state.resume_text = parse_docx(uploaded_file)
            else:
                st.session_state.resume_text = uploaded_file.read().decode("utf-8")

            st.session_state.parsed_resume = parse_resume_to_json(
                st.session_state.resume_text
            )
            st.success("✅ Resume loaded successfully!")

    if st.session_state.resume_text:
        st.metric("Words", len(st.session_state.resume_text.split()))
        st.metric("Characters", len(st.session_state.resume_text))

# Main content
if not st.session_state.resume_text:
    st.info("👈 Please upload your resume in the sidebar to get started")

    st.markdown("### 🎯 What You'll Get:")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **📊 Analysis & Scoring**
        - ATS Compatibility Scan
        - 50+ Point Resume Grading
        - Skills Gap Analysis
        - Keyword Optimization
        """)

    with col2:
        st.markdown("""
        **✍️ Content Generation**
        - Resume Rewriting
        - Cover Letter Creation
        - Email Templates
        - Social Media Profiles
        """)

    with col3:
        st.markdown("""
        **💼 Career Tools**
        - Salary Estimation
        - Interview Prep
        - Job Matching
        - Version Management
        """)
else:
    # Create tabs for different features
    tabs = st.tabs(
        [
            "📊 Grade & Analyze",
            "🎯 Job Matcher",
            "🤖 ATS Scanner",
            "✍️ Rewrite Resume",
            "💼 Cover Letter",
            "📧 Email Templates",
            "🎤 Interview Prep",
            "📈 Skills Analysis",
            "🌐 Social Profiles",
            "💰 Salary Estimate",
            "📑 Version Manager",
        ]
    )

    # TAB 1: Grade & Analyze
    with tabs[0]:
        st.header("📊 Resume Grading & 6-Second Scan")

        col1, col2 = st.columns([2, 1])

        with col1:
            if st.button("Grade My Resume", type="primary", key="grade_resume_btn"):
                grader = ResumeGrader()

                with st.spinner("Analyzing resume..."):
                    # Get file format
                    file_format = (
                        uploaded_file.name.split(".")[-1]
                        if uploaded_file
                        else "unknown"
                    )

                    # Grade resume
                    results = grader.grade_resume(
                        st.session_state.resume_text, file_format
                    )

                    # Display overall score
                    st.markdown("### Overall Grade")
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("Total Score", f"{results['total_score']}/100")
                    with col_b:
                        st.metric("Letter Grade", results["grade"])
                    with col_c:
                        st.metric(
                            "Status",
                            "Pass" if results["total_score"] >= 70 else "Needs Work",
                        )

                    st.info(results["summary"])

                    # Category scores
                    st.markdown("### Category Breakdown")

                    categories = [
                        "content",
                        "formatting",
                        "impact",
                        "ats_compatibility",
                    ]
                    cat_labels = [
                        "Content Quality",
                        "Formatting",
                        "Impact & Results",
                        "ATS Compatible",
                    ]

                    for cat, label in zip(categories, cat_labels):
                        score = results[cat]["score"]
                        st.markdown(f"**{label}:** {score}/100")
                        st.progress(score / 100)

                        with st.expander(f"View {label} Feedback"):
                            for item in results[cat]["feedback"]:
                                st.markdown(f"- {item}")

                    # Top improvements
                    st.markdown("### 🎯 Top Priority Improvements")
                    for i, improvement in enumerate(results["top_improvements"], 1):
                        st.markdown(f"{i}. {improvement}")

        with col2:
            st.markdown("### 👁️ 6-Second Scan Test")
            st.markdown("_What recruiters see in 6 seconds_")

            if st.button("Run 6-Second Scan", key="run_6_second_scan_btn"):
                grader = ResumeGrader()
                scan_results = grader.simulate_6_second_scan(
                    st.session_state.resume_text
                )

                st.metric("Scan Score", f"{scan_results['score']}/100")

                if scan_results["passes_scan"]:
                    st.success("✅ Passes the test!")
                else:
                    st.warning("⚠️ Needs improvement")

                st.markdown("**Quick Checks:**")
                for check, passed in scan_results["checks"].items():
                    icon = "✅" if passed else "❌"
                    st.markdown(f"{icon} {check.replace('_', ' ').title()}")

                with st.expander("View First Screen"):
                    st.text(scan_results["first_screen_preview"])

    # TAB 2: Job Matcher
    with tabs[1]:
        st.header("🎯 Job Description Matcher")

        job_description = st.text_area(
            "Paste Job Description",
            height=200,
            placeholder="Paste the full job description here...",
        )

        if st.button("Analyze Match", type="primary", key="analyze_match_btn") and job_description:
            matcher = JobMatcher()

            with st.spinner("Analyzing match..."):
                # Calculate match score
                match_result = matcher.calculate_match_score(
                    st.session_state.resume_text, job_description
                )

                # Display match score
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Match Score", f"{match_result['match_percentage']}%")
                with col2:
                    st.metric("Matched Keywords", len(match_result["matched_keywords"]))
                with col3:
                    st.metric("Missing Keywords", len(match_result["missing_keywords"]))

                # Match status
                if match_result["match_percentage"] >= 70:
                    st.success("🎉 Excellent match! You're a strong candidate.")
                elif match_result["match_percentage"] >= 50:
                    st.warning("⚠️ Good match, but consider optimizing your resume.")
                else:
                    st.error("❌ Low match. Significant optimization needed.")

                # Keywords breakdown
                col_a, col_b = st.columns(2)

                with col_a:
                    st.markdown("### ✅ Matched Keywords")
                    for kw in match_result["matched_keywords"][:10]:
                        st.markdown(f"- {kw}")

                with col_b:
                    st.markdown("### ❌ Missing Keywords")
                    for kw in match_result["missing_keywords"][:10]:
                        st.markdown(f"- {kw}")

                # Skills gap analysis
                gaps = matcher.identify_skill_gaps(
                    st.session_state.resume_text, job_description
                )

                st.markdown("### 🔍 Skills Gap Analysis")

                gap_categories = [
                    "technical_skills",
                    "tools",
                    "soft_skills",
                    "certifications",
                ]
                gap_labels = [
                    "Technical Skills",
                    "Tools & Technologies",
                    "Soft Skills",
                    "Certifications",
                ]

                for cat, label in zip(gap_categories, gap_labels):
                    if gaps.get(cat):
                        with st.expander(f"{label} ({len(gaps[cat])} gaps)"):
                            for item in gaps[cat]:
                                st.markdown(f"- {item}")

                # Tailoring suggestions
                suggestions = matcher.generate_tailored_suggestions(
                    st.session_state.resume_text, job_description
                )

                st.markdown("### 💡 Tailoring Suggestions")
                for i, suggestion in enumerate(suggestions, 1):
                    st.markdown(
                        f"{i}. **{suggestion['category']}:** {suggestion['suggestion']}"
                    )

                # Generate AI prompt for rewriting
                st.markdown("### 🤖 AI Rewrite Prompt")
                with st.expander("View customization prompt"):
                    prompt = matcher.generate_customized_resume_prompt(
                        st.session_state.resume_text, job_description
                    )
                    st.code(prompt, language="text")

    # TAB 3: ATS Scanner
    with tabs[2]:
        st.header("🤖 ATS Compatibility Scanner")

        col1, col2 = st.columns([2, 1])

        with col1:
            if st.button("Scan for ATS Compatibility", type="primary", key="scan_ats_compatibility_btn"):
                scanner = ATSScanner()

                with st.spinner("Scanning resume..."):
                    file_format = (
                        uploaded_file.name.split(".")[-1] if uploaded_file else "txt"
                    )
                    results = scanner.scan_resume(
                        st.session_state.resume_text, file_format
                    )

                    # Overall score
                    st.metric(
                        "ATS Compatibility Score", f"{results['overall_score']}/100"
                    )

                    if results["overall_score"] >= 80:
                        st.success("✅ Excellent ATS compatibility!")
                    elif results["overall_score"] >= 60:
                        st.warning("⚠️ Good, but room for improvement")
                    else:
                        st.error("❌ Poor ATS compatibility - needs work")

                    # Category results
                    st.markdown("### Scan Results")

                    categories = [
                        "format",
                        "sections",
                        "keywords",
                        "contact_info",
                        "formatting",
                    ]
                    for cat in categories:
                        if cat in results:
                            st.markdown(f"**{cat.replace('_', ' ').title()}**")
                            for item in results[cat]:
                                st.markdown(f"- {item}")
                            st.markdown("---")

                    # Recommendations
                    if "recommendations" in results:
                        st.markdown("### 🎯 Recommendations")
                        for rec in results["recommendations"]:
                            st.info(rec)

        with col2:
            st.markdown("### 🏢 Test Against ATS Systems")

            if st.button("Simulate ATS Systems", key="simulate_ats_systems_btn"):
                scanner = ATSScanner()
                systems = scanner.simulate_ats_systems(st.session_state.resume_text)

                st.markdown("**Compatibility by System:**")

                for system, data in systems.items():
                    score = data["score"]
                    status = data["status"]
                    notes = data.get("notes", "")

                    if score >= 80:
                        icon = "✅"
                    elif score >= 60:
                        icon = "⚠️"
                    else:
                        icon = "❌"

                    st.markdown(f"{icon} **{system}:** {score}% - *{status}*")
                    if notes:
                        st.caption(notes)

    # TAB 4: Rewrite Resume
    with tabs[3]:
        st.header("✍️ AI-Powered Resume Rewriting")

        rewrite_option = st.radio(
            "Choose rewrite style:",
            [
                "Standard Optimization",
                "Job-Specific Tailoring",
                "Industry Change",
                "Career Level Upgrade",
            ],
        )

        if rewrite_option == "Job-Specific Tailoring":
            target_job = st.text_area("Target Job Description", height=150)
        elif rewrite_option == "Industry Change":
            col_a, col_b = st.columns(2)
            with col_a:
                current_industry = st.text_input("Current Industry")
            with col_b:
                target_industry = st.text_input("Target Industry")
        elif rewrite_option == "Career Level Upgrade":
            target_level = st.selectbox(
                "Target Level",
                ["Mid-Level", "Senior", "Lead", "Manager", "Director", "Executive"],
            )

        if st.button("Rewrite Resume", type="primary", key="rewrite_resume_btn"):
            rewriter = ResumeRewriter()

            with st.spinner("Rewriting resume..."):
                if rewrite_option == "Standard Optimization":
                    rewritten = rewriter.rewrite_resume(st.session_state.parsed_resume)
                elif rewrite_option == "Job-Specific Tailoring" and target_job:
                    rewritten = rewriter.tailor_to_job(
                        st.session_state.parsed_resume, target_job
                    )
                # Add other rewrite options here
                else:
                    rewritten = rewriter.rewrite_resume(st.session_state.parsed_resume)

                st.markdown("### ✨ Rewritten Resume")
                st.text_area("Result", rewritten, height=400)

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.download_button(
                        "📥 Download TXT",
                        rewritten,
                        file_name="rewritten_resume.txt",
                        mime="text/plain",
                    )
                with col2:
                    if st.button("💾 Save as Version", key="save_as_version_btn"):
                        version_manager = VersionManager()
                        version_id = version_manager.create_version(
                            rewritten,
                            version_name=f"{rewrite_option}",
                            notes=f"Rewritten using {rewrite_option}",
                        )
                        st.session_state.versions[version_id] = {
                            "content": rewritten,
                            "name": rewrite_option,
                        }
                        st.success(f"Saved as version: {version_id}")

    # TAB 5: Cover Letter
    with tabs[4]:
        st.header("💼 Cover Letter Generator")

        col1, col2 = st.columns(2)
        with col1:
            company_name = st.text_input("Company Name")
            position_title = st.text_input("Position Title")
        with col2:
            hiring_manager = st.text_input("Hiring Manager Name (if known)")
            tone = st.selectbox(
                "Tone", ["Professional", "Enthusiastic", "Technical", "Creative"]
            )

        job_desc_cl = st.text_area("Job Description (optional)", height=150)

        if st.button("Generate Cover Letter", type="primary", key="generate_cover_letter_rewrite_btn"):
            # This would integrate with your existing cover letter agent
            st.info(
                "Cover letter generation would use your existing coverletter_agent.py"
            )

    # TAB 6: Email Templates
    with tabs[5]:
        st.header("📧 Professional Email Templates")

        email_type = st.selectbox(
            "Email Type",
            [
                "Cold Recruiter Outreach",
                "LinkedIn Connection Request",
                "Follow-Up After Application",
                "Thank You After Interview",
                "Networking Request",
                "Referral Request",
                "Salary Negotiation",
                "Rejection Response",
            ],
        )

        generator = EmailGenerator()

        if email_type == "Cold Recruiter Outreach":
            col1, col2 = st.columns(2)
            with col1:
                recruiter_name = st.text_input("Recruiter Name")
                company = st.text_input("Company")
            with col2:
                position = st.text_input("Position")
                your_name = st.text_input("Your Name")

            your_expertise = st.text_input("Your Expertise (brief)")
            tone_email = st.select_slider(
                "Tone", ["Professional", "Confident", "Casual"]
            )

            if st.button("Generate Email", key="generate_email_btn"):
                email = generator.generate_recruiter_email(
                    recruiter_name,
                    company,
                    position,
                    your_name,
                    your_expertise,
                    tone_email.lower(),
                )
                st.text_area("Generated Email", email, height=300)

                # Analyze effectiveness
                analysis = generator.analyze_email_effectiveness(email)
                st.metric("Effectiveness Score", f"{analysis['score']}/100")
                st.markdown("**Feedback:**")
                for feedback in analysis["feedback"]:
                    st.markdown(f"- {feedback}")

        elif email_type == "Thank You After Interview":
            col1, col2 = st.columns(2)
            with col1:
                interviewer_name = st.text_input("Interviewer Name")
                position_ty = st.text_input("Position")
            with col2:
                company_ty = st.text_input("Company")
                your_name_ty = st.text_input("Your Name")

            discussion_point = st.text_input("Specific Discussion Point")

            if st.button("Generate Thank You Email", key="generate_thank_you_email_btn"):
                email = generator.generate_thank_you_email(
                    interviewer_name,
                    position_ty,
                    company_ty,
                    discussion_point,
                    your_name_ty,
                )
                st.text_area("Generated Email", email, height=300)

        # Add more email types as needed

    # TAB 7: Interview Prep
    with tabs[6]:
        st.header("🎤 Interview Preparation")

        if st.button("Generate Interview Questions", type="primary", key="generate_interview_questions_rewrite_btn"):
            prep = InterviewPrep()

            with st.spinner("Generating questions..."):
                questions = prep.generate_questions(st.session_state.resume_text)

                # Display by category
                categories = [
                    ("behavioral", "🎯 Behavioral Questions"),
                    ("technical", "💻 Technical Questions"),
                    ("situational", "🤔 Situational Questions"),
                    ("experience_based", "📋 Experience-Based Questions"),
                    ("achievements", "🏆 Achievement Questions"),
                ]

                for cat, label in categories:
                    with st.expander(f"{label} ({len(questions[cat])} questions)"):
                        for i, q in enumerate(questions[cat], 1):
                            st.markdown(f"**{i}.** {q}")

        st.markdown("---")
        st.markdown("### 🌟 STAR Method Guide")

        if st.button("Get STAR Templates", key="get_star_templates_btn"):
            prep = InterviewPrep()
            templates = prep.generate_star_templates(st.session_state.resume_text)

            for template in templates:
                with st.expander(f"STAR Example: {template['situation'][:50]}..."):
                    st.markdown(f"**Situation:** {template['situation']}")
                    st.markdown(f"**Task:** {template['task']}")
                    st.markdown(f"**Action:** {template['action']}")
                    st.markdown(f"**Result:** {template['result']}")

        st.markdown("---")
        st.markdown("### ❓ Questions to Ask Interviewer")

        if st.button("Get Questions to Ask", key="get_questions_to_ask_btn"):
            prep = InterviewPrep()
            questions_to_ask = prep.generate_questions_to_ask()

            for category, qs in questions_to_ask.items():
                st.markdown(f"**{category.replace('_', ' ').title()}:**")
                for q in qs:
                    st.markdown(f"- {q}")

    # TAB 8: Skills Analysis
    with tabs[7]:
        st.header("📈 Skills Gap Analysis")

        target_role = st.text_input("Target Role/Job Description (optional)")

        if st.button("Analyze Skills", type="primary", key="analyze_skills_btn"):
            analyzer = SkillsAnalyzer()

            with st.spinner("Analyzing skills..."):
                # Extract current skills
                skills = analyzer.extract_skills(st.session_state.resume_text)

                st.markdown("### Your Current Skills")

                for category, skill_list in skills.items():
                    if skill_list:
                        st.markdown(f"**{category}:**")
                        st.markdown(", ".join(skill_list))

                # Gap analysis if target role provided
                if target_role:
                    st.markdown("---")
                    st.markdown("### Skills Gap Analysis")

                    gaps = analyzer.analyze_skill_gaps(
                        st.session_state.resume_text, target_role
                    )

                    for category, data in gaps.items():
                        # data may be a dict with keys or a numeric match percentage
                        if isinstance(data, dict):
                            match_pct = data.get("match_percentage", 0.0)
                            gaps_list = data.get("gaps", [])
                        else:
                            # If upstream returned a numeric value, treat it as match percentage
                            try:
                                match_pct = float(data)
                            except Exception:
                                match_pct = 0.0
                            gaps_list = []

                        st.markdown(f"**{category}:** {match_pct}% match")
                        # guard against division by zero or invalid values
                        try:
                            st.progress(max(0.0, min(1.0, float(match_pct) / 100.0)))
                        except Exception:
                            pass

                        if gaps_list:
                            st.markdown(f"_Missing:_ {', '.join(gaps_list[:5])}")

                # Learning paths
                st.markdown("---")
                st.markdown("### 📚 Recommended Learning Paths")

                if target_role:
                    target_skills = target_role
                else:
                    target_skills = "Python, React, AWS, Docker"  # Default

                paths = analyzer.suggest_learning_paths(
                    st.session_state.resume_text, target_skills
                )

                for path in paths:
                    with st.expander(
                        f"📖 {path['skill']} - {path['priority']} Priority"
                    ):
                        st.markdown(f"**Current Level:** {path['current_level']}")
                        st.markdown(f"**Target Level:** {path['target_level']}")
                        st.markdown(f"**Estimated Time:** {path['estimated_time']}")

                        st.markdown("**Resources:**")
                        for resource in path["resources"]:
                            st.markdown(f"- {resource}")

                # Certifications
                st.markdown("---")
                st.markdown("### 🎓 Recommended Certifications")

                certs = analyzer.recommend_certifications(st.session_state.resume_text)

                for cert in certs:
                    with st.expander(
                        f"🏅 {cert['name']} - {cert['priority']} Priority"
                    ):
                        st.markdown(f"**Provider:** {cert['provider']}")
                        st.markdown(f"**Cost:** {cert['cost']}")
                        st.markdown(f"**Time:** {cert['time_investment']}")
                        st.markdown(f"**Salary Boost:** {cert['salary_boost']}")
                        st.markdown(f"**Prerequisites:** {cert['prerequisites']}")
                        st.markdown(f"**Why:** {cert['relevance_reason']}")

    # TAB 9: Social Profiles
    with tabs[8]:
        st.header("🌐 Social Media Profile Generator")

        platform = st.selectbox(
            "Platform",
            ["LinkedIn", "Twitter", "GitHub", "Portfolio Website", "All Platforms"],
        )

        social_gen = SocialResumeGenerator()

        if platform == "LinkedIn":
            st.markdown("### LinkedIn Profile")

            col1, col2 = st.columns(2)
            with col1:
                name_li = st.text_input(
                    "Name", st.session_state.parsed_resume.get("name", "")
                )
                title_li = st.text_input(
                    "Title", st.session_state.parsed_resume.get("current_role", "")
                )
            with col2:
                years_exp = st.number_input("Years Experience", 1, 50, 5)

            if st.button("Generate LinkedIn Profile", key="generate_linkedin_profile_btn"):
                # Headline
                headline = social_gen.generate_linkedin_headline(
                    title_li, "Technology Innovation", "Driving Results"
                )
                st.markdown("**Headline:**")
                st.info(headline)

                # About section
                about = social_gen.generate_linkedin_about(
                    name_li,
                    title_li,
                    years_exp,
                    st.session_state.parsed_resume.get("skills", [])[:5],
                    ["Increased efficiency by 40%", "Led team of 10"],
                    "I'm passionate about leveraging technology to create impact.",
                )
                st.markdown("**About Section:**")
                st.text_area("LinkedIn About", about, height=300)

        elif platform == "GitHub":
            st.markdown("### GitHub Profile")

            focus_area = st.text_input("Focus Area", "Full-Stack Development")
            languages = st.multiselect(
                "Languages",
                ["Python", "JavaScript", "TypeScript", "Java", "Go", "Rust", "C++"],
                ["Python", "JavaScript"],
            )

            if st.button("Generate GitHub Profile", key="generate_github_profile_btn"):
                bio = social_gen.generate_github_bio(focus_area, languages)
                st.markdown("**GitHub Bio:**")
                st.info(bio)

                readme = social_gen.generate_github_readme_profile(
                    st.session_state.parsed_resume.get("name", "Your Name"),
                    "Software Developer",
                    languages + ["React", "Node.js", "Docker"],
                    "Building awesome open-source projects",
                    "I love solving complex problems with simple solutions",
                )
                st.markdown("**GitHub Profile README:**")
                st.code(readme, language="markdown")

        elif platform == "All Platforms":
            if st.button("Generate All Profiles", key="generate_all_profiles_btn"):
                profiles = social_gen.generate_all_profiles(
                    {
                        "name": st.session_state.parsed_resume.get(
                            "name", "Professional"
                        ),
                        "title": st.session_state.parsed_resume.get(
                            "current_role", "Your Title"
                        ),
                        "skills": st.session_state.parsed_resume.get("skills", []),
                        "years_experience": 5,
                    }
                )

                for platform_name, content in profiles.items():
                    with st.expander(f"📱 {platform_name.replace('_', ' ').title()}"):
                        st.text(content)

    # TAB 10: Salary Estimate
    with tabs[9]:
        st.header("💰 Salary Estimation & Negotiation")

        col1, col2 = st.columns(2)
        with col1:
            job_title_sal = st.text_input(
                "Job Title", st.session_state.parsed_resume.get("current_role", "")
            )
            years_exp_sal = st.number_input("Years Experience", 0, 50, 5)
            education_sal = st.selectbox(
                "Education",
                ["High School", "Associate", "Bachelor's", "Master's", "PhD"],
            )
        with col2:
            location_sal = st.text_input("Location", "San Francisco, CA")
            company_size = st.selectbox(
                "Company Size", ["Startup", "Small", "Medium", "Large/Enterprise"]
            )

        skills_sal = st.multiselect(
            "Key Skills",
            [
                "Python",
                "AWS",
                "React",
                "Machine Learning",
                "Kubernetes",
                "Docker",
                "Go",
                "Rust",
                "Java",
            ],
            ["Python", "AWS"],
        )

        if st.button("Estimate Salary", type="primary", key="estimate_salary_rewrite_btn"):
            estimator = SalaryEstimator()

            with st.spinner("Calculating market value..."):
                estimate = estimator.estimate_salary(
                    job_title_sal,
                    years_exp_sal,
                    skills_sal,
                    education_sal,
                    location_sal,
                    company_size.lower(),
                )

                # Display range
                st.markdown("### 💵 Estimated Salary Range")

                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Minimum", f"${estimate['estimated_range']['min']:,}")
                with col_b:
                    st.metric("Median", f"${estimate['estimated_range']['median']:,}")
                with col_c:
                    st.metric("Maximum", f"${estimate['estimated_range']['max']:,}")

                st.info(f"**Confidence Level:** {estimate['confidence']}")

                # Breakdown
                with st.expander("💡 View Salary Breakdown"):
                    st.markdown("**Calculation Steps:**")
                    for step, value in estimate["breakdown"].items():
                        st.markdown(f"- {step.replace('_', ' ').title()}: ${value:,}")

                # Contributing skills
                if estimate["top_skills_contributing"]:
                    st.markdown("### 🎯 Top Skills Contributing to Salary")
                    for skill_data in estimate["top_skills_contributing"]:
                        st.markdown(
                            f"- **{skill_data['skill']}**: {skill_data['premium_formatted']}"
                        )

                # Negotiation tools
                st.markdown("---")
                st.markdown("### 🤝 Negotiation Tools")

                current_offer = st.number_input(
                    "Current Offer/Salary",
                    min_value=0,
                    value=estimate["estimated_range"]["median"],
                )

                if current_offer > 0:
                    comparison = estimator.compare_to_market(
                        current_offer, estimate["estimated_range"]
                    )

                    st.markdown(
                        f"**Status:** {comparison['status'].replace('_', ' ').title()}"
                    )
                    st.info(comparison["message"])
                    st.markdown(f"**Recommendation:** {comparison['recommendation']}")

                # Negotiation script
                if st.button("Generate Negotiation Script", key="generate_negotiation_script_btn"):
                    target = st.number_input(
                        "Target Salary", value=estimate["estimated_range"]["max"]
                    )

                    script = estimator.generate_negotiation_script(
                        current_offer,
                        target,
                        [
                            f"{years_exp_sal} years of experience",
                            f"Expertise in {', '.join(skills_sal[:3])}",
                            f"Market research shows range of {estimate['formatted_range']}",
                        ],
                    )

                    st.markdown("### 📝 Negotiation Script")
                    st.text_area("Use this script", script, height=300)

    # TAB 11: Version Manager
    with tabs[10]:
        st.header("📑 Resume Version Manager & A/B Testing")

        version_manager = VersionManager()

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("### Current Versions")

            if st.session_state.versions:
                for version_id, data in st.session_state.versions.items():
                    with st.expander(f"📄 {data['name']} (ID: {version_id})"):
                        st.text_area(
                            "Content",
                            data["content"],
                            height=200,
                            key=f"ver_{version_id}",
                        )

                        # Track performance
                        st.markdown("**Track Performance:**")
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            applications = st.number_input(
                                "Applications", 0, 1000, 0, key=f"app_{version_id}"
                            )
                        with col_b:
                            interviews = st.number_input(
                                "Interviews", 0, 100, 0, key=f"int_{version_id}"
                            )
                        with col_c:
                            offers = st.number_input(
                                "Offers", 0, 50, 0, key=f"off_{version_id}"
                            )

                        if st.button("Update Performance", key=f"upd_{version_id}"):
                            version_manager.update_performance(
                                version_id,
                                applications,
                                interviews,
                                interviews,
                                0,
                                offers,
                            )
                            st.success("Performance updated!")
            else:
                st.info(
                    "No versions saved yet. Create versions in the 'Rewrite Resume' tab."
                )

        with col2:
            st.markdown("### Analytics")

            if len(st.session_state.versions) >= 2:
                version_ids = list(st.session_state.versions.keys())
                version_1 = st.selectbox("Version 1", version_ids, key="v1")
                version_2 = st.selectbox("Version 2", version_ids, key="v2")

                if st.button("Compare Versions", key="compare_versions_btn"):
                    comparison = version_manager.compare_versions(version_1, version_2)

                    st.markdown("**Winner:** " + comparison["winner"])

                    for version, metrics in comparison["versions"].items():
                        st.markdown(f"**{version}:**")
                        st.markdown(f"- Response Rate: {metrics['response_rate']}%")
                        st.markdown(f"- Interview Rate: {metrics['interview_rate']}%")
                        st.markdown(f"- Offer Rate: {metrics['offer_rate']}%")

st.markdown("---")
st.markdown("Built with ❤️ using Streamlit | All features integrated and ready to use!")
