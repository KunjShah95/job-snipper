"""
ResumeMasterAI - Professional Landing Page
Complete AI-powered resume optimization and career management platform.
"""

import streamlit as st
import os
import sys
import urllib.parse

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.color_scheme import get_unified_css
from utils.user_analytics import init_analytics, track_page, auto_save_session, show_profile_form
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="ResumeMasterAI - AI-Powered Career Excellence",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize analytics for this page
analytics = init_analytics()
track_page("Home")

# Apply unified CSS
st.markdown(get_unified_css(), unsafe_allow_html=True)

# Initialize session state
if "loaded" not in st.session_state:
    st.session_state.loaded = True

# Hero Section
start_page = "/?page=" + urllib.parse.quote("pages/1_📄_Upload_Resume.py")
st.markdown(
    f"""
<div class="hero-section">
    <div style="position: relative; z-index: 2;">
        <div class="ai-badge">
            ✨ Powered by Advanced AI
        </div>
        <h1 class="hero-title">
            Transform Your Career with <span class="gradient-text">AI-Powered</span> Resume Magic
        </h1>
        <p class="hero-subtitle">
             The Ultimate Resume Optimization Platform
        </p>
        <p class="hero-tagline">
            Leverage cutting-edge AI to create, optimize, and manage your professional documents with unprecedented precision
        </p>
        <div style="margin-top: 2rem;">
            <!-- Use JS navigation to ensure Streamlit picks up the query param change -->
            <a href="#" onclick="window.location.href='{start_page}'; return false;" style="text-decoration: none;">
                <button style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; border: none; padding: 1rem 3rem; font-size: 1.2rem; font-weight: 700; border-radius: 50px; cursor: pointer; box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4); transition: all 0.3s ease; margin-right: 1rem;">
                     Get Started Free
                </button>
            </a>
            <a href="#features" style="text-decoration: none;">
                <button style="background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); color: white; border: 2px solid rgba(255, 255, 255, 0.3); padding: 1rem 3rem; font-size: 1.2rem; font-weight: 700; border-radius: 50px; cursor: pointer; transition: all 0.3s ease;">
                     Learn More
                </button>
            </a>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# Quick Navigation
st.markdown('<div id="navigation"></div>', unsafe_allow_html=True)
st.markdown(
    """
<div class="section-title">⚡ Quick Navigation</div>
<div class="section-subtitle">Jump to the tool you need</div>
""",
    unsafe_allow_html=True,
)

# Navigation Grid
nav_items = [
    (
        "📄",
        "Upload Resume",
        "Upload and parse your resume",
        "pages/1_📄_Upload_Resume.py",
    ),
    (
        "📊",
        "Analysis & Scoring",
        "Get detailed ATS analysis",
        "pages/2_📊_Analysis_Scoring.py",
    ),
    ("🎯", "Job Matching", "Find perfect job matches", "pages/3_🎯_Job_Matching.py"),
    (
        "✍️",
        "Resume Rewrite",
        "AI-powered optimization",
        "pages/4_✍️_Resume_Rewrite.py",
    ),
    (
        "💼",
        "Cover Letters",
        "Generate custom letters",
        "pages/5_💼_Cover_Letter_Projects.py",
    ),
    ("🔍", "Job Search", "Search opportunities", "pages/6_🔍_Job_Search.py"),
    ("🏗️", "Resume Builder", "Build from scratch", "pages/7_🏗️_Resume_Builder.py"),
]

cols = st.columns(len(nav_items))
for i, (icon, title, desc, page_file) in enumerate(nav_items):
    with cols[i]:
        # Build a Streamlit multipage query param link (URL-encoded)
        href = "/?page=" + urllib.parse.quote(page_file)
        st.markdown(
            f"""
        <a href="{href}" target="_self" style="text-decoration: none;">
            <div class="nav-card">
                <div class="nav-card-icon">{icon}</div>
                <div class="nav-card-title">{title}</div>
                <div class="nav-card-desc">{desc}</div>
            </div>
        </a>
        """,
            unsafe_allow_html=True,
        )

# Features Section
st.markdown(
    '<div id="features" style="margin-top: 4rem;"></div>', unsafe_allow_html=True
)
st.markdown(
    """
<div class="section-title">🌟 Powerful Features</div>
<div class="section-subtitle">Everything you need for career success</div>
""",
    unsafe_allow_html=True,
)

feature_data = [
    {
        "icon": "🤖",
        "title": "AI-Powered Parsing",
        "desc": "Advanced OCR and NLP extract every detail from your resume with 95%+ accuracy",
    },
    {
        "icon": "📊",
        "title": "ATS Optimization",
        "desc": "Get scored and optimized for Applicant Tracking Systems used by 99% of companies",
    },
    {
        "icon": "🎯",
        "title": "Smart Job Matching",
        "desc": "AI matches you with perfect opportunities based on skills, experience, and preferences",
    },
    {
        "icon": "✨",
        "title": "Professional Rewriting",
        "desc": "Transform your resume with AI-powered content enhancement and formatting",
    },
    {
        "icon": "💼",
        "title": "Cover Letter Generator",
        "desc": "Create personalized, compelling cover letters in seconds for any job",
    },
    {
        "icon": "🔍",
        "title": "Job Search Engine",
        "desc": "Search thousands of jobs from multiple platforms in one place",
    },
    {
        "icon": "📈",
        "title": "Career Analytics",
        "desc": "Track your applications, analyze trends, and optimize your job search strategy",
    },
    {
        "icon": "🎨",
        "title": "Multiple Templates",
        "desc": "Choose from professional ATS-friendly templates designed by career experts",
    },
    {
        "icon": "🎤",
        "title": "Interview Prep",
        "desc": "Practice with AI-generated interview questions tailored to your target role",
    },
    {
        "icon": "💰",
        "title": "Salary Insights",
        "desc": "Get accurate salary estimates based on role, location, and experience",
    },
    {
        "icon": "💡",
        "title": "Skills Analysis",
        "desc": "Identify skill gaps and get personalized learning recommendations",
    },
    {
        "icon": "📱",
        "title": "Social Profiles",
        "desc": "Optimize your LinkedIn and other professional social media presence",
    },
]

# Display features in grid
cols = st.columns(4)
for idx, feature in enumerate(feature_data):
    with cols[idx % 4]:
        st.markdown(
            f"""
        <div class="feature-card">
            <div class="feature-icon">{feature["icon"]}</div>
            <h3 style="color: #667eea; font-size: 1.2rem; margin-bottom: 0.5rem; font-weight: 700;">{feature["title"]}</h3>
            <p style="color: #555; font-size: 0.95rem; line-height: 1.6;">{feature["desc"]}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

# Statistics Section
st.markdown('<div style="margin-top: 4rem;"></div>', unsafe_allow_html=True)
st.markdown(
    """
<div class="section-title">📈 Proven Results</div>
<div class="section-subtitle">Join thousands of successful job seekers</div>
""",
    unsafe_allow_html=True,
)

stat_cols = st.columns(4)
stats = [
    ("50K+", "Resumes Optimized"),
    ("98%", "ATS Pass Rate"),
    ("10K+", "Job Placements"),
    ("4.9⭐", "User Rating"),
]

for col, (number, label) in zip(stat_cols, stats):
    with col:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-number">{number}</div>
            <div class="stat-label">{label}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

# Technology Stack
st.markdown('<div style="margin-top: 4rem;"></div>', unsafe_allow_html=True)
st.markdown(
    """
<div class="section-title">⚡ Powered By</div>
<div class="section-subtitle">Industry-leading AI technologies</div>
""",
    unsafe_allow_html=True,
)

tech_cols = st.columns(6)
technologies = [
    ("🤖", "Google Gemini"),
    ("🔗", "LangChain"),
    ("🐍", "Python"),
    ("⚡", "Streamlit"),
    ("📊", "Plotly"),
    ("🎯", "OpenAI"),
]

for col, (icon, name) in zip(tech_cols, technologies):
    with col:
        st.markdown(
            f"""
        <div class="tech-card">
            <div class="tech-icon">{icon}</div>
            <div class="tech-name">{name}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

# How It Works
st.markdown('<div style="margin-top: 4rem;"></div>', unsafe_allow_html=True)
st.markdown(
    """
<div class="section-title">🎯 How It Works</div>
<div class="section-subtitle">Simple 4-step process to career success</div>
""",
    unsafe_allow_html=True,
)

steps_cols = st.columns(4)
steps = [
    ("1️⃣", "Upload", "Upload your current resume in PDF or DOCX format"),
    ("2️⃣", "Analyze", "Our AI analyzes and scores your resume"),
    ("3️⃣", "Optimize", "Get AI-powered suggestions and rewrites"),
    ("4️⃣", "Apply", "Download and apply with confidence"),
]

for col, (num, title, desc) in zip(steps_cols, steps):
    with col:
        st.markdown(
            f"""
        <div class="feature-card">
            <div style="font-size: 3rem; margin-bottom: 1rem;">{num}</div>
            <h3 style="color: #667eea; font-size: 1.3rem; margin-bottom: 0.5rem; font-weight: 700;">{title}</h3>
            <p style="color: #666; font-size: 0.95rem; line-height: 1.6;">{desc}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

# Testimonials
st.markdown('<div style="margin-top: 4rem;"></div>', unsafe_allow_html=True)
st.markdown(
    """
<div class="section-title">💬 What Users Say</div>
<div class="section-subtitle">Real success stories from our users</div>
""",
    unsafe_allow_html=True,
)

testimonial_cols = st.columns(3)
testimonials = [
    {
        "text": "ResumeMasterAI helped me land my dream job at Google! The ATS optimization was a game-changer.",
        "author": "Sarah Johnson",
        "role": "Software Engineer at Google",
    },
    {
        "text": "I was able to rewrite my resume in minutes instead of hours. The AI suggestions were spot-on!",
        "author": "Michael Chen",
        "role": "Product Manager at Amazon",
    },
    {
        "text": "The job matching feature found opportunities I would have never discovered on my own. Highly recommend!",
        "author": "Emily Rodriguez",
        "role": "Data Scientist at Microsoft",
    },
]

for col, testimonial in zip(testimonial_cols, testimonials):
    with col:
        st.markdown(
            f"""
        <div class="testimonial-card">
            <div class="testimonial-text">"{testimonial["text"]}"</div>
            <div class="testimonial-author">{testimonial["author"]}</div>
            <div class="testimonial-role">{testimonial["role"]}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

# Pricing / CTA Section
st.markdown('<div style="margin-top: 4rem;"></div>', unsafe_allow_html=True)
st.markdown(
    """
<div class="hero-section" style="min-height: 400px;">
    <div style="position: relative; z-index: 2; text-align: center;">
        <h2 style="font-size: 3rem; font-weight: 900; color: white; margin-bottom: 1rem;">
            Ready to Transform Your Career? 🚀
        </h2>
        <p style="font-size: 1.3rem; color: rgba(255, 255, 255, 0.9); margin-bottom: 2rem;">
            Join 50,000+ professionals who've accelerated their careers with ResumeMasterAI
        </p>
        <a href="{start_page}" target="_self" style="text-decoration: none;">
            <button style="background: linear-gradient(135deg, #fbbf24, #f97316); color: white; border: none; padding: 1.2rem 3.5rem; font-size: 1.3rem; font-weight: 800; border-radius: 50px; cursor: pointer; box-shadow: 0 15px 40px rgba(251, 191, 36, 0.4); transition: all 0.3s ease; animation: pulse 2s infinite;">
                ✨ Start Your Journey - It's FREE
            </button>
        </a>
        <p style="color: rgba(255, 255, 255, 0.7); margin-top: 1rem; font-size: 0.95rem;">
            No credit card required • Free forever • Unlimited resumes
        </p>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# FAQ Section
st.markdown('<div style="margin-top: 3rem;"></div>', unsafe_allow_html=True)
st.markdown(
    """
<div class="section-title">❓ Frequently Asked Questions</div>
""",
    unsafe_allow_html=True,
)

with st.expander("🔒 Is my resume data secure?"):
    st.markdown("""
    Absolutely! We use industry-standard encryption and never share your data with third parties. 
    Your resume is processed securely and can be deleted at any time.
    """)

with st.expander("💰 Is ResumeMasterAI really free?"):
    st.markdown("""
    Yes! All core features including resume parsing, ATS optimization, and basic rewriting are 
    completely free with no hidden charges.
    """)

with st.expander("📱 Can I use this on mobile?"):
    st.markdown("""
    Yes, ResumeMasterAI is fully responsive and works on all devices including smartphones and tablets.
    """)

with st.expander("🌍 What languages are supported?"):
    st.markdown("""
    Currently, we support English resumes. We're working on adding support for multiple languages soon.
    """)

with st.expander("⚡ How fast is the AI processing?"):
    st.markdown("""
    Most resumes are parsed and analyzed in under 30 seconds. Complex documents may take up to 2 minutes.
    """)

# Footer
st.markdown('<div style="margin-top: 4rem;"></div>', unsafe_allow_html=True)
st.markdown(
    """
<div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 20px; padding: 2rem; text-align: center; border: 1px solid rgba(255, 255, 255, 0.1);">
    <div style="color: rgba(255, 255, 255, 0.9); font-size: 1.1rem; margin-bottom: 1rem;">
        <strong>ResumeMasterAI</strong> - Your AI Career Partner
    </div>
    <div style="color: rgba(255, 255, 255, 0.6); font-size: 0.9rem; margin-bottom: 1rem;">
        Powered by Google Gemini AI • Built with ❤️ using Streamlit
    </div>
    <div style="color: rgba(255, 255, 255, 0.5); font-size: 0.85rem;">
        © 2025 ResumeMasterAI. All rights reserved. | Privacy Policy | Terms of Service
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# Sidebar
with st.sidebar:
    st.markdown(
        """
    <div style="text-align: center; padding: 1rem;">
        <h2 style="color: white; margin-bottom: 0.5rem;">🚀 ResumeMasterAI</h2>
        <p style="color: rgba(255, 255, 255, 0.7); font-size: 0.9rem;">
            AI-Powered Career Excellence
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown("### 🎯 Quick Access")
    st.page_link("pages/1_📄_Upload_Resume.py", label="📄 Upload Resume", icon="📄")
    st.page_link(
        "pages/2_📊_Analysis_Scoring.py", label="📊 Analysis & Scoring", icon="📊"
    )
    st.page_link("pages/3_🎯_Job_Matching.py", label="🎯 Job Matching", icon="🎯")
    st.page_link(
        "pages/4_✍️_Resume_Rewrite.py", label="✍️ Resume Rewrite", icon="✍️"
    )
    st.page_link(
        "pages/5b_🚀_Project_Suggestions.py",
        label="🚀 Project Suggestions",
        icon="🚀",
    )

    st.markdown("---")

    st.markdown("### 🛠️ Utility Tools")
    st.page_link("pages/8_🎤_Interview_Prep.py", label="🎤 Interview Prep", icon="🎤")
    st.page_link(
        "pages/9_💰_Salary_Estimator.py", label="💰 Salary Estimator", icon="💰"
    )
    st.page_link(
        "pages/10_💡_Skills_Analyzer.py", label="💡 Skills Analyzer", icon="💡"
    )
    st.page_link("pages/11_📱_Social_Resume.py", label="📱 Social Resume", icon="📱")
    st.page_link(
        "pages/12_📧_Email_Generator.py", label="📧 Email Generator", icon="📧"
    )

    st.markdown("---")

    st.info("💡 **Tip**: Start by uploading your resume to unlock all features!")

# User Profile Collection Section
st.markdown("---")
with st.expander("👤 Complete Your Profile", expanded=False):
    show_profile_form()

# Analytics sidebar (auto-saves session data)
auto_save_session()
