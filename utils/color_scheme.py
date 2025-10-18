"""
Unified Color Scheme Configuration for ResumeMasterAI
All pages should use these consistent colors for a professional look
"""

import os

# Primary Brand Colors
PRIMARY_GRADIENT_START = "#667eea"
PRIMARY_GRADIENT_END = "#764ba2"
PRIMARY_GRADIENT = (
    f"linear-gradient(135deg, {PRIMARY_GRADIENT_START} 0%, {PRIMARY_GRADIENT_END} 100%)"
)

# Secondary Colors
SECONDARY_GRADIENT_START = "#2E86AB"
SECONDARY_GRADIENT_END = "#06A77D"
SECONDARY_GRADIENT = f"linear-gradient(135deg, {SECONDARY_GRADIENT_START} 0%, {SECONDARY_GRADIENT_END} 100%)"

# Accent Colors
ACCENT_ORANGE = "#F18F01"
ACCENT_PINK_START = "#f093fb"
ACCENT_PINK_END = "#f5576c"
ACCENT_PINK_GRADIENT = (
    f"linear-gradient(135deg, {ACCENT_PINK_START} 0%, {ACCENT_PINK_END} 100%)"
)

# Status Colors
SUCCESS_GREEN = "#06A77D"
WARNING_ORANGE = "#F18F01"
DANGER_RED = "#C73E1D"
INFO_BLUE = "#2E86AB"

# Neutral Colors
BACKGROUND_LIGHT = "#F8F9FA"
CARD_BACKGROUND = "#FFFFFF"
TEXT_PRIMARY = "#2D3142"
TEXT_SECONDARY = "#4F5D75"
BORDER_COLOR = "#E5E5E5"

# Dark Mode Colors (for prefers-color-scheme: dark)
DARK_BACKGROUND = "#1a1a2e"
DARK_CARD = "#16213e"
DARK_TEXT_PRIMARY = "#eaeaea"
DARK_TEXT_SECONDARY = "#bfbfbf"

# Shadow and Effects
SHADOW_SM = "0 2px 8px rgba(0,0,0,0.08)"
SHADOW_MD = "0 4px 12px rgba(0,0,0,0.1)"
SHADOW_LG = "0 8px 24px rgba(0,0,0,0.12)"
GLASS_EFFECT = "backdrop-filter: blur(10px); background: rgba(255, 255, 255, 0.9);"


def get_unified_css():
    """
    Returns unified CSS that should be applied to all pages
    This creates a consistent, professional design across the entire platform
    """
    return f"""
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&display=swap');
    
    /* ==================== GLOBAL STYLES ==================== */
    * {{
        font-family: 'Inter', sans-serif;
        box-sizing: border-box;
    }}
    
    /* Streamlit Branding visibility (toggle with env HIDE_STREAMLIT_BRANDING=1) */
    {"/* Hidden by environment setting */\n    #MainMenu {visibility: hidden;}\n    footer {visibility: hidden;}\n    header {visibility: hidden;}\n    .stDeployButton {display: none;}" if os.getenv('HIDE_STREAMLIT_BRANDING','0') in ('1','true','True','yes') else ""}
    
    /* Main App Background */
    .stApp {{
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        background-attachment: fixed;
    }}
    
    .main {{
        background: transparent;
    }}
    
    /* Block Container */
    .block-container {{
        padding: 2rem 1rem;
        max-width: 1400px;
    }}
    
    /* ==================== CARD STYLES ==================== */
    
    /* Unified Card Style */
    .unified-card {{
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.9));
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
        border: 2px solid rgba(102, 126, 234, 0.1);
        margin: 1rem 0;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }}
    
    .unified-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        transition: left 0.5s;
    }}
    
    .unified-card:hover::before {{
        left: 100%;
    }}
    
    .unified-card:hover {{
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 50px rgba(102, 126, 234, 0.25);
        border-color: {PRIMARY_GRADIENT_START};
    }}
    
    /* Feature Card */
    .feature-card {{
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.85));
        border-radius: 25px;
        padding: 2.5rem 2rem;
        text-align: center;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 2px solid transparent;
        position: relative;
        overflow: hidden;
        height: 100%;
    }}
    
    .feature-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.2), transparent);
        transition: left 0.5s;
    }}
    
    .feature-card:hover::before {{
        left: 100%;
    }}
    
    .feature-card:hover {{
        transform: translateY(-12px) scale(1.05);
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
        border-color: {PRIMARY_GRADIENT_START};
    }}
    
    /* Glass Card Style */
    .glass-card {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }}
    
    .glass-card:hover {{
        background: rgba(255, 255, 255, 0.15);
        border-color: rgba(255, 255, 255, 0.3);
        transform: translateY(-5px);
    }}
    
    /* ==================== TYPOGRAPHY ==================== */
    
    /* Gradient Headers */
    .gradient-header {{
        background: {PRIMARY_GRADIENT};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 900;
        font-size: 2.5rem;
        margin-bottom: 1rem;
        letter-spacing: -1px;
    }}
    
    .gradient-text {{
        background: linear-gradient(90deg, #fbbf24 0%, #f97316 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        background-size: 200% auto;
        animation: shimmer 3s linear infinite;
    }}
    
    .section-title {{
        font-size: 3rem;
        font-weight: 900;
        text-align: center;
        margin: 3rem 0 1rem;
        color: white;
        letter-spacing: -2px;
    }}
    
    .section-subtitle {{
        font-size: 1.2rem;
        text-align: center;
        color: rgba(255, 255, 255, 0.8);
        margin-bottom: 3rem;
        font-weight: 400;
    }}
    
    /* ==================== BUTTON STYLES ==================== */
    
    .stButton > button {{
        width: 100%;
        background: {PRIMARY_GRADIENT} !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        cursor: pointer !important;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5) !important;
        background: linear-gradient(135deg, {PRIMARY_GRADIENT_END} 0%, {PRIMARY_GRADIENT_START} 100%) !important;
    }}
    
    .stButton > button:active {{
        transform: translateY(0px) !important;
    }}
    
    /* ==================== BADGE STYLES ==================== */
    
    .badge {{
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.25rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }}
    
    .badge:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }}
    
    .badge-success {{
        background: linear-gradient(135deg, {SUCCESS_GREEN}, #059669);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    }}
    
    .badge-warning {{
        background: linear-gradient(135deg, {WARNING_ORANGE}, #d97706);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);
    }}
    
    .badge-danger {{
        background: linear-gradient(135deg, {DANGER_RED}, #dc2626);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
    }}
    
    .badge-primary {{
        background: {PRIMARY_GRADIENT};
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }}
    
    .ai-badge {{
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1.2rem;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 30px;
        color: white;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        animation: float 3s ease-in-out infinite;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }}
    
    /* ==================== PROGRESS BAR ==================== */
    
    .progress-bar {{
        background: rgba(102, 126, 234, 0.2);
        height: 12px;
        border-radius: 10px;
        overflow: hidden;
        margin: 1rem 0;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
    }}
    
    .progress-fill {{
        background: {PRIMARY_GRADIENT};
        height: 100%;
        transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
    }}
    
    /* ==================== ICON STYLES ==================== */
    
    .social-icon {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 50px;
        height: 50px;
        background: {PRIMARY_GRADIENT};
        border-radius: 50%;
        text-align: center;
        color: white;
        font-size: 1.2rem;
        margin: 0 0.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }}
    
    .social-icon:hover {{
        transform: scale(1.15) rotate(5deg);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
    }}
    
    .feature-icon {{
        font-size: 3rem;
        margin-bottom: 1.5rem;
        background: {PRIMARY_GRADIENT};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        display: inline-block;
    }}
    
    /* ==================== NAVIGATION CARDS ==================== */
    
    .nav-section {{
        padding: 2rem 0;
        margin: 2rem 0;
    }}
    
    .nav-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }}
    
    .nav-card {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem 1.5rem;
        text-align: center;
        border: 2px solid rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }}
    
    .nav-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: {PRIMARY_GRADIENT};
        opacity: 0;
        transition: all 0.5s;
    }}
    
    .nav-card:hover::before {{
        left: 0;
        opacity: 0.1;
    }}
    
    .nav-card:hover {{
        transform: translateY(-10px) scale(1.05);
        border-color: {PRIMARY_GRADIENT_START};
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.3);
    }}
    
    .nav-card-icon {{
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }}
    
    .nav-card-title {{
        font-size: 1.1rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.5rem;
    }}
    
    .nav-card-desc {{
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.7);
        line-height: 1.5;
    }}
    
    /* ==================== INPUT FIELDS ==================== */
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {{
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }}
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {{
        border-color: {PRIMARY_GRADIENT_START} !important;
        box-shadow: 0 0 15px rgba(102, 126, 234, 0.3) !important;
        background: rgba(255, 255, 255, 0.15) !important;
    }}
    
    .stTextInput > label,
    .stTextArea > label,
    .stSelectbox > label {{
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
    }}
    
    /* ==================== FILE UPLOADER ==================== */
    
    .stFileUploader > div {{
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border: 2px dashed rgba(255, 255, 255, 0.3) !important;
        border-radius: 15px !important;
        padding: 2rem !important;
        transition: all 0.3s ease !important;
    }}
    
    .stFileUploader > div:hover {{
        border-color: {PRIMARY_GRADIENT_START} !important;
        background: rgba(255, 255, 255, 0.15) !important;
    }}
    
    /* ==================== TABS ==================== */
    
    .stTabs [data-baseweb="tab-list"] {{
        gap: 1rem;
        background: transparent;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background: rgba(255, 255, 255, 0.15);
        border-color: {PRIMARY_GRADIENT_START};
    }}
    
    .stTabs [aria-selected="true"] {{
        background: {PRIMARY_GRADIENT} !important;
        border-color: {PRIMARY_GRADIENT_START} !important;
        color: white !important;
    }}
    
    /* ==================== EXPANDER ==================== */
    
    .streamlit-expanderHeader {{
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 1rem 1.5rem !important;
        transition: all 0.3s ease !important;
    }}
    
    .streamlit-expanderHeader:hover {{
        background: rgba(255, 255, 255, 0.15) !important;
        border-color: {PRIMARY_GRADIENT_START} !important;
    }}
    
    /* ==================== DATAFRAME ==================== */
    
    .stDataFrame {{
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 15px !important;
        overflow: hidden !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15) !important;
    }}
    
    /* ==================== METRICS ==================== */
    
    [data-testid="stMetricValue"] {{
        font-size: 2rem !important;
        font-weight: 900 !important;
        background: {PRIMARY_GRADIENT};
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }}
    
    [data-testid="stMetricLabel"] {{
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }}
    
    /* ==================== ALERTS ==================== */
    
    /* Success Alert - Green theme with dark text */
    div[data-baseweb="notification"][kind="success"],
    .stAlert[data-baseweb="notification"][kind="success"] {{
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%) !important;
        border: 2px solid #28a745 !important;
        border-radius: 15px !important;
        color: #155724 !important;
        padding: 1rem 1.5rem !important;
        font-weight: 600 !important;
    }}
    
    /* Info Alert - Blue theme with dark text */
    div[data-baseweb="notification"][kind="info"],
    .stAlert[data-baseweb="notification"][kind="info"] {{
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%) !important;
        border: 2px solid #17a2b8 !important;
        border-radius: 15px !important;
        color: #0c5460 !important;
        padding: 1rem 1.5rem !important;
        font-weight: 600 !important;
    }}
    
    /* Warning Alert - Orange theme with dark text */
    div[data-baseweb="notification"][kind="warning"],
    .stAlert[data-baseweb="notification"][kind="warning"] {{
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%) !important;
        border: 2px solid #ffc107 !important;
        border-radius: 15px !important;
        color: #856404 !important;
        padding: 1rem 1.5rem !important;
        font-weight: 600 !important;
    }}
    
    /* Error Alert - Red theme with dark text */
    div[data-baseweb="notification"][kind="error"],
    .stAlert[data-baseweb="notification"][kind="error"] {{
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%) !important;
        border: 2px solid #dc3545 !important;
        border-radius: 15px !important;
        color: #721c24 !important;
        padding: 1rem 1.5rem !important;
        font-weight: 600 !important;
    }}
    
    /* Generic Alert fallback */
    .stAlert {{
        background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e0 100%) !important;
        border-radius: 15px !important;
        border: 2px solid #4a5568 !important;
        color: #1a202c !important;
        padding: 1rem 1.5rem !important;
        font-weight: 600 !important;
    }}
    
    /* ==================== SIDEBAR ==================== */
    
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%) !important;
    }}
    
    [data-testid="stSidebar"] .stMarkdown {{
        color: rgba(255, 255, 255, 0.9) !important;
    }}
    
    /* Dark Mode Support */
    @media (prefers-color-scheme: dark) {{
        .main {{
            background: {DARK_BACKGROUND};
        }}
        
        .unified-card, .glass-card {{
            background: {DARK_CARD};
            color: {DARK_TEXT_PRIMARY};
            border-color: rgba(255, 255, 255, 0.1);
        }}
        
        .unified-card:hover {{
            box-shadow: 0 8px 24px rgba(0,0,0,0.3);
        }}
    }}
    
    /* ==================== HERO SECTION ==================== */
    
    .hero-section {{
        padding: 4rem 2rem;
        text-align: center;
        position: relative;
        min-height: 600px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, 
            rgba(102, 126, 234, 0.1) 0%,
            rgba(118, 75, 162, 0.1) 50%,
            rgba(102, 126, 234, 0.05) 100%);
        border-radius: 30px;
        margin: 2rem 0;
        overflow: hidden;
    }}
    
    .hero-section::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 70%);
        animation: gradientShift 15s ease infinite;
    }}
    
    .hero-title {{
        font-size: 4rem;
        font-weight: 900;
        color: white;
        margin-bottom: 1rem;
        line-height: 1.2;
        letter-spacing: -2px;
        position: relative;
        z-index: 2;
    }}
    
    .hero-subtitle {{
        font-size: 1.5rem;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 1rem;
        font-weight: 400;
        position: relative;
        z-index: 2;
    }}
    
    .hero-tagline {{
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.7);
        margin-bottom: 2rem;
        font-weight: 300;
        position: relative;
        z-index: 2;
    }}
    
    /* ==================== STATISTICS CARDS ==================== */
    
    .stat-card {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }}
    
    .stat-card:hover {{
        background: rgba(255, 255, 255, 0.15);
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }}
    
    .stat-number {{
        font-size: 3rem;
        font-weight: 900;
        background: {PRIMARY_GRADIENT};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }}
    
    .stat-label {{
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 600;
    }}
    
    /* ==================== TECHNOLOGY CARDS ==================== */
    
    .tech-card {{
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        height: 100%;
    }}
    
    .tech-card:hover {{
        background: rgba(255, 255, 255, 0.15);
        transform: translateY(-8px);
        border-color: {PRIMARY_GRADIENT_START};
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
    }}
    
    .tech-icon {{
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }}
    
    .tech-name {{
        font-size: 1rem;
        font-weight: 600;
        color: white;
    }}
    
    /* ==================== TESTIMONIAL CARDS ==================== */
    
    .testimonial-card {{
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.9));
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
        border-left: 4px solid {PRIMARY_GRADIENT_START};
        transition: all 0.3s ease;
        height: 100%;
    }}
    
    .testimonial-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.25);
    }}
    
    .testimonial-text {{
        font-size: 1rem;
        color: #333;
        line-height: 1.8;
        margin-bottom: 1.5rem;
        font-style: italic;
    }}
    
    .testimonial-author {{
        font-weight: 700;
        color: {PRIMARY_GRADIENT_START};
        margin-bottom: 0.25rem;
    }}
    
    .testimonial-role {{
        font-size: 0.9rem;
        color: #666;
    }}
    
    /* ==================== ANIMATIONS ==================== */
    
    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(30px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    .animate-fade-in {{
        animation: fadeInUp 0.6s ease-out;
    }}
    
    @keyframes pulse {{
        0%, 100% {{
            opacity: 1;
        }}
        50% {{
            opacity: 0.7;
        }}
    }}
    
    .animate-pulse {{
        animation: pulse 2s infinite;
    }}
    
    @keyframes float {{
        0%, 100% {{
            transform: translateY(0px);
        }}
        50% {{
            transform: translateY(-10px);
        }}
    }}
    
    @keyframes shimmer {{
        0% {{
            background-position: -200% center;
        }}
        100% {{
            background-position: 200% center;
        }}
    }}
    
    @keyframes gradientShift {{
        0%, 100% {{
            transform: rotate(0deg) scale(1);
        }}
        50% {{
            transform: rotate(180deg) scale(1.2);
        }}
    }}
    
    @keyframes moveParticles {{
        0% {{
            transform: translateY(0) translateX(0);
        }}
        100% {{
            transform: translateY(-100vh) translateX(50px);
        }}
    }}
    </style>
    """


def get_gradio_css():
    """
    Return a compact CSS string intended for Gradio apps.
    Keep it minimal to avoid interfering with Streamlit styles.
    """
    return """
    /* Gradio specific minimal styling */
    body { background: #0f1724; font-family: Inter, system-ui, sans-serif; }
    .gradio-container { max-width: 1200px; margin: 20px auto; }
    .gradio-container .header { background: linear-gradient(90deg, #2b6cb0 0%, #805ad5 100%); color: white; padding: 18px; border-radius: 8px; }
    .gr-button { border-radius: 8px; padding: 10px 16px; }
    .gr-button-primary { background: linear-gradient(90deg,#2b6cb0,#805ad5); color: white; }
    .gradio-container .footer { color: #e6eef8; margin-top: 18px; }
    """
