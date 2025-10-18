"""
Resume Builder Page
Build a professional resume from scratch with a guided form interface.
"""

import streamlit as st
import os
import sys
import uuid
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.color_scheme import get_unified_css
from utils.document_export import export_to_docx, export_to_pdf
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Resume Builder - ResumeMasterAI", page_icon="🏗️", layout="wide"
)

# Apply unified color scheme
st.markdown(get_unified_css(), unsafe_allow_html=True)

# Initialize session state for builder
if "builder_data" not in st.session_state:
    st.session_state.builder_data = {
        "personal": {},
        "summary": "",
        "experience": [],
        "education": [],
        "skills": [],
        "certifications": [],
        "projects": [],
    }

if "preview_mode" not in st.session_state:
    st.session_state.preview_mode = False

# Header
st.markdown("# 🏗️ Resume Builder")
st.markdown(
    """
<div class="custom-card">
    <p style="font-size: 1.1rem; color: #4F5D75;">
        Build a professional resume from scratch using our guided form interface. 
        Fill in your details, and we'll format it beautifully for you!
    </p>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# Toggle between edit and preview mode
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    if st.button(
        "👁️ Preview Resume" if not st.session_state.preview_mode else "✏️ Edit Resume",
        use_container_width=True,
        type="primary",
        key="toggle_preview_btn",
    ):
        st.session_state.preview_mode = not st.session_state.preview_mode
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Edit Mode
if not st.session_state.preview_mode:
    # Personal Information Section
    st.markdown("## 👤 Personal Information")

    col1, col2 = st.columns(2)

    with col1:
        full_name = st.text_input(
            "Full Name *",
            value=st.session_state.builder_data["personal"].get("name", ""),
            placeholder="John Doe",
        )
        email = st.text_input(
            "Email *",
            value=st.session_state.builder_data["personal"].get("email", ""),
            placeholder="john.doe@example.com",
        )
        phone = st.text_input(
            "Phone Number *",
            value=st.session_state.builder_data["personal"].get("phone", ""),
            placeholder="+1 (555) 123-4567",
        )

    with col2:
        location = st.text_input(
            "Location *",
            value=st.session_state.builder_data["personal"].get("location", ""),
            placeholder="San Francisco, CA",
        )
        portfolio = st.text_input(
            "Portfolio/Website",
            value=st.session_state.builder_data["personal"].get("portfolio", ""),
            placeholder="https://www.johndoe.com",
        )
        title = st.text_input(
            "Professional Title",
            value=st.session_state.builder_data["personal"].get("title", ""),
            placeholder="Senior Software Engineer",
        )

    # Social Media Links
    st.markdown("### 🔗 Social Media & Professional Links")

    col1, col2, col3 = st.columns(3)

    with col1:
        linkedin = st.text_input(
            "🔗 LinkedIn",
            value=st.session_state.builder_data["personal"].get("linkedin", ""),
            placeholder="https://linkedin.com/in/johndoe",
        )
        github = st.text_input(
            "💻 GitHub",
            value=st.session_state.builder_data["personal"].get("github", ""),
            placeholder="https://github.com/johndoe",
        )

    with col2:
        twitter = st.text_input(
            "🐦 Twitter/X",
            value=st.session_state.builder_data["personal"].get("twitter", ""),
            placeholder="https://twitter.com/johndoe",
        )
        medium = st.text_input(
            "📝 Medium/Blog",
            value=st.session_state.builder_data["personal"].get("medium", ""),
            placeholder="https://medium.com/@johndoe",
        )

    with col3:
        stackoverflow = st.text_input(
            "📚 Stack Overflow",
            value=st.session_state.builder_data["personal"].get("stackoverflow", ""),
            placeholder="https://stackoverflow.com/users/...",
        )
        other_link = st.text_input(
            "🌐 Other Link",
            value=st.session_state.builder_data["personal"].get("other_link", ""),
            placeholder="https://...",
        )

    # Save personal info
    st.session_state.builder_data["personal"] = {
        "name": full_name,
        "email": email,
        "phone": phone,
        "location": location,
        "portfolio": portfolio,
        "title": title,
        "linkedin": linkedin,
        "github": github,
        "twitter": twitter,
        "medium": medium,
        "stackoverflow": stackoverflow,
        "other_link": other_link,
    }

    st.markdown("<br>", unsafe_allow_html=True)

    # Professional Summary
    st.markdown("## 📝 Professional Summary")
    summary = st.text_area(
        "Write a brief summary of your professional background (2-3 sentences)",
        value=st.session_state.builder_data["summary"],
        height=120,
        placeholder="Experienced software engineer with 5+ years in full-stack development...",
    )
    st.session_state.builder_data["summary"] = summary

    st.markdown("<br>", unsafe_allow_html=True)

    # Work Experience
    st.markdown("## 💼 Work Experience")

    num_experiences = st.number_input(
        "Number of Work Experiences",
        min_value=0,
        max_value=10,
        value=len(st.session_state.builder_data["experience"]),
    )

    experiences = []
    for i in range(num_experiences):
        with st.expander(f"Experience #{i + 1}", expanded=i == 0):
            col1, col2 = st.columns(2)

            with col1:
                job_title = st.text_input(
                    "Job Title *",
                    key=f"exp_title_{i}",
                    value=st.session_state.builder_data["experience"][i].get(
                        "title", ""
                    )
                    if i < len(st.session_state.builder_data["experience"])
                    else "",
                )
                company = st.text_input(
                    "Company *",
                    key=f"exp_company_{i}",
                    value=st.session_state.builder_data["experience"][i].get(
                        "company", ""
                    )
                    if i < len(st.session_state.builder_data["experience"])
                    else "",
                )

            with col2:
                start_date = st.text_input(
                    "Start Date *",
                    key=f"exp_start_{i}",
                    value=st.session_state.builder_data["experience"][i].get(
                        "start_date", ""
                    )
                    if i < len(st.session_state.builder_data["experience"])
                    else "",
                    placeholder="Jan 2020",
                )
                end_date = st.text_input(
                    "End Date",
                    key=f"exp_end_{i}",
                    value=st.session_state.builder_data["experience"][i].get(
                        "end_date", ""
                    )
                    if i < len(st.session_state.builder_data["experience"])
                    else "",
                    placeholder="Present",
                )

            responsibilities = st.text_area(
                "Key Responsibilities & Achievements (one per line, starting with • or -)",
                key=f"exp_resp_{i}",
                value=st.session_state.builder_data["experience"][i].get(
                    "responsibilities", ""
                )
                if i < len(st.session_state.builder_data["experience"])
                else "",
                height=150,
                placeholder="• Led a team of 5 developers...\n• Increased performance by 40%...",
            )

            experiences.append(
                {
                    "title": job_title,
                    "company": company,
                    "start_date": start_date,
                    "end_date": end_date,
                    "responsibilities": responsibilities,
                }
            )

    st.session_state.builder_data["experience"] = experiences

    st.markdown("<br>", unsafe_allow_html=True)

    # Education
    st.markdown("## 🎓 Education")

    num_education = st.number_input(
        "Number of Education Entries",
        min_value=0,
        max_value=5,
        value=len(st.session_state.builder_data["education"]),
    )

    education = []
    for i in range(num_education):
        with st.expander(f"Education #{i + 1}", expanded=i == 0):
            col1, col2 = st.columns(2)

            with col1:
                degree = st.text_input(
                    "Degree *",
                    key=f"edu_degree_{i}",
                    value=st.session_state.builder_data["education"][i].get(
                        "degree", ""
                    )
                    if i < len(st.session_state.builder_data["education"])
                    else "",
                    placeholder="Bachelor of Science in Computer Science",
                )
                institution = st.text_input(
                    "Institution *",
                    key=f"edu_inst_{i}",
                    value=st.session_state.builder_data["education"][i].get(
                        "institution", ""
                    )
                    if i < len(st.session_state.builder_data["education"])
                    else "",
                    placeholder="Stanford University",
                )

            with col2:
                grad_year = st.text_input(
                    "Graduation Year",
                    key=f"edu_year_{i}",
                    value=st.session_state.builder_data["education"][i].get("year", "")
                    if i < len(st.session_state.builder_data["education"])
                    else "",
                    placeholder="2020",
                )
                gpa = st.text_input(
                    "GPA (optional)",
                    key=f"edu_gpa_{i}",
                    value=st.session_state.builder_data["education"][i].get("gpa", "")
                    if i < len(st.session_state.builder_data["education"])
                    else "",
                    placeholder="3.8/4.0",
                )

            education.append(
                {
                    "degree": degree,
                    "institution": institution,
                    "year": grad_year,
                    "gpa": gpa,
                }
            )

    st.session_state.builder_data["education"] = education

    st.markdown("<br>", unsafe_allow_html=True)

    # Skills
    st.markdown("## 🛠️ Skills")

    col1, col2 = st.columns(2)

    with col1:
        technical_skills = st.text_area(
            "Technical Skills (comma-separated)",
            value=", ".join(
                st.session_state.builder_data["skills"][
                    : len(st.session_state.builder_data["skills"]) // 2
                ]
            )
            if st.session_state.builder_data["skills"]
            else "",
            height=100,
            placeholder="Python, JavaScript, React, Node.js, AWS, Docker",
        )

    with col2:
        soft_skills = st.text_area(
            "Soft Skills (comma-separated)",
            value=", ".join(
                st.session_state.builder_data["skills"][
                    len(st.session_state.builder_data["skills"]) // 2 :
                ]
            )
            if st.session_state.builder_data["skills"]
            else "",
            height=100,
            placeholder="Leadership, Communication, Problem Solving, Team Collaboration",
        )

    all_skills = []
    if technical_skills:
        all_skills.extend([s.strip() for s in technical_skills.split(",")])
    if soft_skills:
        all_skills.extend([s.strip() for s in soft_skills.split(",")])

    st.session_state.builder_data["skills"] = all_skills

    st.markdown("<br>", unsafe_allow_html=True)

    # Optional Sections
    with st.expander("➕ Add Certifications", expanded=False):
        st.markdown("**Add professional certifications with verification links**")
        num_certs = st.number_input(
            "Number of Certifications",
            min_value=0,
            max_value=10,
            value=len(st.session_state.builder_data["certifications"]),
        )

        certifications = []
        for i in range(num_certs):
            st.markdown(f"**Certification #{i + 1}**")
            col1, col2, col3 = st.columns(3)
            with col1:
                cert_name = st.text_input(
                    "Certification Name",
                    key=f"cert_name_{i}",
                    value=st.session_state.builder_data["certifications"][i].get(
                        "name", ""
                    )
                    if i < len(st.session_state.builder_data["certifications"])
                    else "",
                    placeholder="AWS Certified Solutions Architect",
                )
            with col2:
                cert_issuer = st.text_input(
                    "Issuing Organization",
                    key=f"cert_issuer_{i}",
                    value=st.session_state.builder_data["certifications"][i].get(
                        "issuer", ""
                    )
                    if i < len(st.session_state.builder_data["certifications"])
                    else "",
                    placeholder="Amazon Web Services",
                )
            with col3:
                cert_year = st.text_input(
                    "Year Obtained",
                    key=f"cert_year_{i}",
                    value=st.session_state.builder_data["certifications"][i].get(
                        "year", ""
                    )
                    if i < len(st.session_state.builder_data["certifications"])
                    else "",
                    placeholder="2024",
                )

            cert_link = st.text_input(
                "🔗 Certificate Verification Link (optional)",
                key=f"cert_link_{i}",
                value=st.session_state.builder_data["certifications"][i].get("link", "")
                if i < len(st.session_state.builder_data["certifications"])
                else "",
                placeholder="https://www.credly.com/badges/...",
            )

            if cert_name:
                certifications.append(
                    {
                        "name": cert_name,
                        "issuer": cert_issuer,
                        "year": cert_year,
                        "link": cert_link,
                    }
                )

            if i < num_certs - 1:
                st.markdown("---")

        st.session_state.builder_data["certifications"] = certifications

    with st.expander("➕ Add Projects"):
        num_projects = st.number_input(
            "Number of Projects",
            min_value=0,
            max_value=10,
            value=len(st.session_state.builder_data["projects"]),
        )

        projects = []
        for i in range(num_projects):
            proj_name = st.text_input(
                "Project Name",
                key=f"proj_name_{i}",
                value=st.session_state.builder_data["projects"][i].get("name", "")
                if i < len(st.session_state.builder_data["projects"])
                else "",
            )
            proj_desc = st.text_area(
                "Project Description",
                key=f"proj_desc_{i}",
                value=st.session_state.builder_data["projects"][i].get(
                    "description", ""
                )
                if i < len(st.session_state.builder_data["projects"])
                else "",
                height=80,
            )

            if proj_name:
                projects.append({"name": proj_name, "description": proj_desc})

        st.session_state.builder_data["projects"] = projects

# Preview Mode
else:
    data = st.session_state.builder_data

    # Generate resume text
    resume_text = ""

    # Personal Info Header
    personal = data["personal"]
    if personal.get("name"):
        resume_text += f"{personal['name'].upper()}\n"
        if personal.get("title"):
            resume_text += f"{personal['title']}\n"

        contact_parts = []
        if personal.get("email"):
            contact_parts.append(personal["email"])
        if personal.get("phone"):
            contact_parts.append(personal["phone"])
        if personal.get("location"):
            contact_parts.append(personal["location"])
        if contact_parts:
            resume_text += " | ".join(contact_parts) + "\n"

        # Social Media Links
        social_links = []
        if personal.get("linkedin"):
            social_links.append(f"LinkedIn: {personal['linkedin']}")
        if personal.get("github"):
            social_links.append(f"GitHub: {personal['github']}")
        if personal.get("portfolio"):
            social_links.append(f"Portfolio: {personal['portfolio']}")
        if personal.get("twitter"):
            social_links.append(f"Twitter: {personal['twitter']}")
        if personal.get("medium"):
            social_links.append(f"Blog: {personal['medium']}")
        if personal.get("stackoverflow"):
            social_links.append(f"Stack Overflow: {personal['stackoverflow']}")
        if personal.get("other_link"):
            social_links.append(f"Other: {personal['other_link']}")

        if social_links:
            resume_text += "\n".join(social_links) + "\n"

        resume_text += "\n"

    # Professional Summary
    if data["summary"]:
        resume_text += "PROFESSIONAL SUMMARY\n"
        resume_text += f"{data['summary']}\n\n"

    # Work Experience
    if data["experience"]:
        resume_text += "WORK EXPERIENCE\n"
        for exp in data["experience"]:
            if exp.get("title") and exp.get("company"):
                resume_text += f"\n{exp['title']} | {exp['company']}\n"
                if exp.get("start_date"):
                    date_range = (
                        f"{exp['start_date']} - {exp.get('end_date', 'Present')}"
                    )
                    resume_text += f"{date_range}\n"
                if exp.get("responsibilities"):
                    resume_text += f"{exp['responsibilities']}\n"
        resume_text += "\n"

    # Education
    if data["education"]:
        resume_text += "EDUCATION\n"
        for edu in data["education"]:
            if edu.get("degree") and edu.get("institution"):
                resume_text += f"\n{edu['degree']}\n"
                resume_text += f"{edu['institution']}"
                if edu.get("year"):
                    resume_text += f" | Graduated: {edu['year']}"
                if edu.get("gpa"):
                    resume_text += f" | GPA: {edu['gpa']}"
                resume_text += "\n"
        resume_text += "\n"

    # Skills
    if data["skills"]:
        resume_text += "SKILLS\n"
        resume_text += ", ".join(data["skills"]) + "\n\n"

    # Certifications
    if data["certifications"]:
        resume_text += "CERTIFICATIONS\n"
        for cert in data["certifications"]:
            if cert.get("name"):
                cert_line = f"• {cert['name']}"
                if cert.get("issuer"):
                    cert_line += f" - {cert['issuer']}"
                if cert.get("year"):
                    cert_line += f" ({cert['year']})"
                if cert.get("link"):
                    cert_line += f"\n  Verify: {cert['link']}"
                resume_text += cert_line + "\n"
        resume_text += "\n"

    # Projects
    if data["projects"]:
        resume_text += "PROJECTS\n"
        for proj in data["projects"]:
            if proj.get("name"):
                resume_text += f"\n{proj['name']}\n"
                if proj.get("description"):
                    resume_text += f"{proj['description']}\n"
        resume_text += "\n"

    # Display preview
    st.markdown("## 📄 Resume Preview")

    st.text_area(
        "Your Resume", value=resume_text, height=600, label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Download options
    st.markdown("## 💾 Download Your Resume")

    from utils.document_export import export_to_docx, export_to_pdf

    col1, col2, col3, col4, col5 = st.columns(5)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    with col1:
        st.download_button(
            label="📄 TXT",
            data=resume_text,
            file_name=f"resume_built_{timestamp}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with col2:
        st.download_button(
            label="📝 MD",
            data=resume_text,
            file_name=f"resume_built_{timestamp}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with col3:
        try:
            contact_info = {
                "email": personal.get("email", ""),
                "phone": personal.get("phone", ""),
                "location": personal.get("location", ""),
            }
            name = personal.get("name", "Resume")

            docx_buffer = export_to_docx(resume_text, name, contact_info)
            st.download_button(
                label="📘 DOCX",
                data=docx_buffer,
                file_name=f"resume_built_{timestamp}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )
        except Exception as e:
            st.button(
                "📘 DOCX",
                disabled=True,
                use_container_width=True,
                help=f"Error: {str(e)}",
            )

    with col4:
        try:
            contact_info = {
                "email": personal.get("email", ""),
                "phone": personal.get("phone", ""),
                "location": personal.get("location", ""),
            }
            name = personal.get("name", "Resume")

            pdf_buffer = export_to_pdf(resume_text, name, contact_info)
            st.download_button(
                label="📕 PDF",
                data=pdf_buffer,
                file_name=f"resume_built_{timestamp}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        except Exception:
            st.button(
                "📕 PDF",
                disabled=True,
                use_container_width=True,
                help="Install reportlab: pip install reportlab",
            )

    with col5:
        if st.button("🔄 New Resume", use_container_width=True, key="new_resume_btn"):
            st.session_state.builder_data = {
                "personal": {},
                "summary": "",
                "experience": [],
                "education": [],
                "skills": [],
                "certifications": [],
                "projects": [],
            }
            st.session_state.preview_mode = False
            st.rerun()

# Progress indicator
st.markdown("---")
st.markdown(
    """
<div style="text-align: center; padding: 1rem;">
    <p style="color: #4F5D75; font-size: 0.9rem;">
        <strong>Step 7 of 7:</strong> Resume Builder
    </p>
    <div style="background: #E5E5E5; height: 6px; border-radius: 3px; overflow: hidden; max-width: 600px; margin: 0.5rem auto;">
        <div style="background: linear-gradient(90deg, #2E86AB 0%, #06A77D 100%); height: 100%; width: 100%;"></div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)
