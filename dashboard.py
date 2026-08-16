import json
import streamlit as st
from app.agent import (
    ask_pathpilot,
    ask_pathpilot_career,
    ask_pathpilot_skillgap,
    ask_pathpilot_with_notes,
)
from app.career import list_job_descriptions, load_job_description
from app.memory import get_weak_topics, mark_as_improved, record_mistake
from app.study import list_notes, load_note

# =========================================================
# PAGE SETUP
# =========================================================
st.set_page_config(
    page_title="PathPilot AI",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# ICON SYSTEM
# =========================================================
def icon(name, size=18, color="currentColor", stroke_width="2"):
    paths = {
        "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/>',
        "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
        "briefcase": '<rect x="2.5" y="7" width="19" height="13" rx="2"/><path d="M15.5 20V5.5a2 2 0 0 0-2-2h-3a2 2 0 0 0-2 2V20"/>',
        "compass": '<circle cx="12" cy="12" r="9.5"/><polygon points="15.5 8.5 13.5 13.5 8.5 15.5 10.5 10.5 15.5 8.5"/>',
        "alert": '<circle cx="12" cy="12" r="9.5"/><line x1="12" y1="7.5" x2="12" y2="12.5"/><line x1="12" y1="16" x2="12.01" y2="16"/>',
        "settings": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>',
        "sparkle": '<path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3z"/>',
        "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"/>',
        "arrow-right": '<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>',
    }
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" '
        f'stroke-linecap="round" stroke-linejoin="round">{paths.get(name, "")}</svg>'
    )


# =========================================================
# GLOBAL STYLING
# =========================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --primary: #0D9488;
        --primary-deep: #0F766E;
        --primary-soft: #E6F4F2;
        --primary-gradient: linear-gradient(135deg, #0F766E 0%, #0D9488 55%, #14B8A6 100%);
        --warn-soft: #FEF2F2;
        --warn-text: #B91C1C;
        --text-main: #1C1917;
        --text-muted: #78716C;
        --border-color: #E7E4DD;
        --app-bg: #FAFAF9;
        --font-display: 'Poppins', sans-serif;
        --font-body: 'Inter', sans-serif;
    }

    html, body, [class*="css"] { font-family: var(--font-body); }
    .stApp { background: var(--app-bg); }
    .block-container {
        padding-top: 1.35rem;
        padding-bottom: 3rem;
        max-width: 1180px;
    }

    header[data-testid="stHeader"] { background: transparent !important; }
    #MainMenu, footer { visibility: hidden; }

    /* ---------------- Responsive Layout Polish ---------------- */

    /* Keep the desktop composition spacious and prevent accidental horizontal overflow. */
    .block-container {
        width: 100% !important;
        box-sizing: border-box !important;
    }

    /* Tablet */
    @media (max-width: 900px) {
        .block-container {
            padding-left: 1.15rem !important;
            padding-right: 1.15rem !important;
        }

        section[data-testid="stSidebar"] {
            min-width: 238px !important;
            max-width: 238px !important;
        }
    }

    /* Phone: let Streamlit control the drawer width and stack dashboard columns. */
    @media (max-width: 768px) {
        .block-container {
            max-width: 100% !important;
            padding-top: 0.9rem !important;
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
            padding-bottom: 2.25rem !important;
        }

        section[data-testid="stSidebar"] {
            min-width: 0 !important;
            width: min(88vw, 320px) !important;
            max-width: min(88vw, 320px) !important;
        }

        section[data-testid="stSidebar"] > div:first-child {
            width: 100% !important;
            box-sizing: border-box !important;
            padding: 0.85rem 0.7rem 1rem 0.7rem !important;
        }

        .brand {
            padding-left: 0.35rem !important;
            padding-right: 0.35rem !important;
            padding-bottom: 0.9rem !important;
        }

        .brand-title {
            font-size: 1.08rem !important;
        }

        .brand-subtitle {
            font-size: 0.65rem !important;
        }

        section[data-testid="stSidebar"] .stButton > button {
            height: 44px !important;
            min-height: 44px !important;
            font-size: 0.84rem !important;
        }

        /* Make Streamlit's horizontal column groups become true mobile stacks. */
        [data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
            gap: 0.75rem !important;
        }

        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
            flex: 1 1 100% !important;
            min-width: 100% !important;
            width: 100% !important;
        }

        /* Keep the hero readable without forcing horizontal scrolling. */
        .hero {
            padding: 1.25rem 1.1rem !important;
            min-height: auto !important;
        }

        .hero-title {
            font-size: clamp(1.35rem, 6vw, 1.8rem) !important;
            line-height: 1.18 !important;
        }

        .hero-text {
            font-size: 0.78rem !important;
            line-height: 1.55 !important;
        }

        .stat-card,
        .feature-card {
            min-height: auto !important;
        }

        .stat-card {
            padding: 1rem !important;
        }

        .feature-card {
            padding: 1.1rem !important;
        }

        /* Prevent long labels/descriptions from creating overflow. */
        .section-title,
        .section-subtitle,
        .feature-title,
        .feature-text,
        .stat-label {
            overflow-wrap: anywhere !important;
        }

        /* Make the ask area comfortable for thumb use. */
        .ask-wrap {
            padding: 0.55rem !important;
        }
    }

    /* Small phones */
    @media (max-width: 480px) {
        .block-container {
            padding-left: 0.65rem !important;
            padding-right: 0.65rem !important;
        }

        .brand-logo {
            width: 34px !important;
            height: 34px !important;
        }

        .brand-title {
            font-size: 1rem !important;
        }

        .nav-label {
            font-size: 0.60rem !important;
        }

        .hero-title {
            font-size: 1.28rem !important;
        }

        .hero-text {
            font-size: 0.74rem !important;
        }
    }

    /* ---------------- Sidebar ---------------- */
    section[data-testid="stSidebar"] {
        background: #FFFFFF !important;
        border-right: 1px solid var(--border-color) !important;
        min-width: 238px !important;
        max-width: 238px !important;
        width: 238px !important;
    }

    section[data-testid="stSidebar"] > div:first-child {
        width: 238px !important;
        padding: 0.9rem 0.8rem 1rem 0.8rem !important;
    }
    .brand {
        display: flex; align-items: center; gap: 10px;
        padding: 0.35rem 0.45rem 1.15rem 0.45rem;
        border-bottom: 1px solid var(--border-color);
        margin-bottom: 0.75rem;
    }
    .brand-logo {
        width: 36px; height: 36px; border-radius: 9px;
        background: var(--primary-gradient);
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 6px 16px rgba(13, 148, 136, 0.28);
    }
    .brand-title {
        font-family: var(--font-display);
        font-size: 1.16rem;
        font-weight: 800;
        color: #171717;
        letter-spacing: -0.025em;
        line-height: 1.15;
    }
    .brand-subtitle {
        color: #78716C;
        font-size: 0.69rem;
        font-weight: 500;
        letter-spacing: 0;
        line-height: 1.35;
        margin-top: 2px;
    }
    .nav-label { color: #A8A29E; font-size: 0.62rem; font-weight: 700; letter-spacing: 0.1em; padding: 0.2rem 0.6rem 0.5rem; }

    /* ---------------- Polished Professional Sidebar ---------------- */
    section[data-testid="stSidebar"] {
        background: #FFFFFF !important;
        border-right: 1px solid #E7ECEA !important;
        box-shadow: 8px 0 28px rgba(15, 23, 42, 0.025) !important;
    }

    section[data-testid="stSidebar"] > div:first-child {
        padding: 0.82rem 0.72rem 0.9rem 0.72rem !important;
    }

    section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0.16rem !important;
    }

    section[data-testid="stSidebar"] [data-testid="element-container"] {
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }

    section[data-testid="stSidebar"] .stButton {
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Navigation buttons */
    section[data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        height: 43px !important;
        min-height: 43px !important;
        margin: 1px 0 !important;
        padding: 0 0.72rem !important;
        border-radius: 9px !important;
        border: 1px solid transparent !important;
        background: transparent !important;
        color: #526174 !important;
        box-shadow: none !important;
        transform: none !important;
        text-align: left !important;
        justify-content: flex-start !important;
        font-family: var(--font-body) !important;
        font-size: 0.84rem !important;
        font-weight: 600 !important;
        letter-spacing: -0.005em !important;
        transition: all 0.16s ease !important;
    }

    section[data-testid="stSidebar"] .stButton > button p {
        margin: 0 !important;
        width: 100% !important;
        text-align: left !important;
        font-family: var(--font-body) !important;
        font-size: 0.84rem !important;
        line-height: 1 !important;
        letter-spacing: 0 !important;
    }

    /* Give the existing compact symbols a consistent product accent */
    section[data-testid="stSidebar"] .stButton > button p::first-letter {
        color: #0D9488 !important;
        font-weight: 700 !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #F4F8F7 !important;
        color: #0F766E !important;
        border-color: #E4EEEC !important;
        box-shadow: none !important;
        transform: translateX(1px) !important;
    }

    /* Active navigation */
    section[data-testid="stSidebar"] .stButton > button[kind="primary"],
    section[data-testid="stSidebar"] .stButton > button[data-testid="baseButton-primary"] {
        background: #EAF7F5 !important;
        color: #0F766E !important;
        border: 1px solid #D7ECE8 !important;
        border-left: 3px solid #0D9488 !important;
        border-radius: 9px !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 8px rgba(13, 148, 136, 0.06) !important;
    }

    section[data-testid="stSidebar"] .stButton > button[kind="primary"] p,
    section[data-testid="stSidebar"] .stButton > button[data-testid="baseButton-primary"] p {
        color: #0F766E !important;
        font-weight: 700 !important;
    }

    section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover,
    section[data-testid="stSidebar"] .stButton > button[data-testid="baseButton-primary"]:hover {
        background: #EAF7F5 !important;
        color: #0F766E !important;
        border-color: #D7ECE8 !important;
        border-left-color: #0D9488 !important;
        transform: none !important;
    }

    /* Navigation heading */
    section[data-testid="stSidebar"] .nav-label {
        color: #98A4A1 !important;
        font-size: 0.65rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.13em !important;
        padding: 0.22rem 0.65rem 0.55rem !important;
        margin: 0 !important;
    }

    /* Divider */
    section[data-testid="stSidebar"] .nav-divider {
        height: 1px !important;
        background: #E8ECEB !important;
        margin: 0.68rem 0.28rem 0.58rem !important;
    }

    /* Profile card */
    section[data-testid="stSidebar"] .sidebar-user {
        margin-top: 0.65rem !important;
        padding: 0.75rem !important;
        border: 1px solid #E3EAE8 !important;
        border-radius: 12px !important;
        background: #FBFDFC !important;
        box-shadow: 0 2px 9px rgba(15, 23, 42, 0.035) !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    }

    section[data-testid="stSidebar"] .sidebar-user:hover {
        border-color: #D6E7E3 !important;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05) !important;
    }

    section[data-testid="stSidebar"] .sidebar-user-avatar {
        width: 35px !important;
        height: 35px !important;
        border-radius: 10px !important;
        background: #E5F5F2 !important;
        color: #0F766E !important;
    }

    section[data-testid="stSidebar"] .sidebar-footer {
        color: #A8B1AE !important;
        font-size: 0.59rem !important;
        line-height: 1.5 !important;
        padding: 0.72rem 0.2rem 0 !important;
        text-align: center !important;
        letter-spacing: 0.015em !important;
    }

    /* ---------------- Inputs: force readable text everywhere ---------------- */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div,
    .stSelectbox div[data-baseweb="select"] span {
        color: var(--text-main) !important;
        background: #FFFFFF !important;
        border: 1px solid var(--border-color) !important;
        caret-color: var(--primary);
    }
    .stTextInput input::placeholder, .stTextArea textarea::placeholder { color: #A8A29E !important; opacity: 1; }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 1px var(--primary) !important;
    }

    .sidebar-user {
        margin-top: 0.9rem; padding: 0.7rem; border: 1px solid var(--border-color);
        border-radius: 12px; background: #FAFAF9; display: flex; align-items: center; gap: 9px;
    }
    .sidebar-user-avatar {
        width: 34px; height: 34px; border-radius: 50%; background: var(--primary-soft);
        color: var(--primary-deep); display: flex; align-items: center; justify-content: center; flex-shrink: 0;
    }
    .sidebar-footer { color: #A8A29E; font-size: 0.64rem; line-height: 1.6; padding: 1rem 0.35rem 0; text-align: center; letter-spacing: 0.02em; }

    /* ---------------- Headings ---------------- */
    .page-heading { font-family: var(--font-display); font-size: 1.55rem; font-weight: 700; color: var(--text-main); margin-bottom: 2px; letter-spacing: -0.015em; }
    .page-subheading { color: var(--text-muted); font-size: 0.9rem; margin-bottom: 1.4rem; }
    .eyebrow { color: var(--primary-deep); font-size: 0.66rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.3rem; }

    /* ---------------- Hero / Form fix ---------------- */
    [data-testid="stForm"] {
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
        padding: 0.4rem !important;
        background: #FFFFFF !important;
    }
    [data-testid="stForm"] .stTextInput input {
        background: #FFFFFF !important;
        border: none !important;
        color: var(--text-main) !important;
        border-radius: 8px !important;
        height: 44px;
    }
    [data-testid="stForm"] .stTextInput input::placeholder { color: #A8A29E !important; }
    [data-testid="stForm"] .stFormSubmitButton button {
        background: var(--primary-gradient) !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        height: 44px !important;
        border: none !important;
    }
    [data-testid="stForm"] .stFormSubmitButton button:hover { opacity: 0.92; }

    /* ---------------- Cards ---------------- */
    .card {
        background: #FFFFFF; border: 1px solid var(--border-color);
        border-radius: 14px; padding: 1.4rem 1.5rem; margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(28, 25, 23, 0.03);
    }
    .feature-card {
        background: #FFFFFF; border: 1px solid var(--border-color);
        border-radius: 14px; padding: 1.3rem; min-height: 145px; margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(28, 25, 23, 0.03); transition: all 0.15s ease;
        border-top: 2px solid transparent;
    }
    .feature-card:hover { transform: translateY(-2px); border-top-color: var(--primary); box-shadow: 0 10px 22px rgba(28, 25, 23, 0.06); }
    .feature-icon {
        width: 34px; height: 34px; border-radius: 8px; background: var(--primary-soft); color: var(--primary-deep);
        display: flex; align-items: center; justify-content: center; margin-bottom: 0.8rem;
    }
    .feature-title { font-family: var(--font-display); color: var(--text-main); font-weight: 600; font-size: 0.93rem; margin-bottom: 0.3rem; }
    .feature-text { color: var(--text-muted); font-size: 0.79rem; line-height: 1.55; }

    /* Native bordered containers (st.container(border=True)) get the same card polish */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px !important;
        border-color: var(--border-color) !important;
        background: #FFFFFF;
        box-shadow: 0 1px 3px rgba(28, 25, 23, 0.03);
    }

    .section-title { font-family: var(--font-display); font-size: 1.08rem; font-weight: 650; color: var(--text-main); margin-bottom: 0.2rem; }
    .section-subtitle { color: var(--text-muted); font-size: 0.8rem; margin-bottom: 1rem; }

    /* ---------------- Stat Cards ---------------- */
    .stat-card {
        background: #FFFFFF; border: 1px solid var(--border-color);
        border-radius: 12px; padding: 1.1rem; box-shadow: 0 1px 2px rgba(28, 25, 23, 0.02);
        transition: transform 0.2s ease; border-bottom: 2px solid var(--primary-soft);
    }
    .stat-card:hover { transform: translateY(-2px); border-bottom-color: var(--primary); }
    .stat-number { font-family: var(--font-display); font-size: 1.55rem; font-weight: 700; color: var(--text-main); margin-top: 0.3rem; }
    .stat-label { font-size: 0.76rem; color: var(--text-muted); font-weight: 600; margin-top: 0.1rem; }

    /* ---------------- Chat bubbles ---------------- */
    .chat-wrap { background:#FFFFFF; border:1px solid var(--border-color); border-radius:14px; padding:1.5rem; margin-bottom:1.5rem; box-shadow:0 4px 10px rgba(28,25,23,0.035); }
    .chat-user { text-align:right; margin-bottom:1rem; }
    .chat-user span { background:var(--primary-soft); color:#0F4D46; border:1px solid #BEE5E0; padding:0.6rem 1rem; border-radius:10px; font-weight:600; font-size:0.88rem; display:inline-block; }
    .chat-ai { background:#FAFAF9; border:1px solid var(--border-color); border-left:3px solid var(--primary); border-radius:10px; padding:1.1rem 1.3rem; color:#292524; font-size:0.9rem; line-height:1.65; margin-bottom:1rem; }

    /* ---------------- Answer box (for feature pages) ---------------- */
    .answer-box {
        background: #FFFFFF; border: 1px solid var(--border-color); border-left: 3px solid var(--primary);
        border-radius: 10px; padding: 1.2rem 1.35rem; margin-top: 1rem; color: #292524;
        line-height: 1.65; box-shadow: 0 5px 16px rgba(28, 25, 23, 0.03);
    }
    .answer-label { font-family: var(--font-display); display: flex; align-items: center; gap: 6px; font-weight: 650; color: var(--text-main); margin-bottom: 0.7rem; font-size: 0.83rem; }

    /* ---------------- Badges ---------------- */
    .badge { display: inline-block; padding: 0.25rem 0.7rem; border-radius: 999px; font-size: 0.7rem; font-weight: 700; margin-right: 0.35rem; }
    .badge-warn { background: var(--warn-soft); color: var(--warn-text); }
    .badge-info { background: var(--primary-soft); color: var(--primary-deep); }

    /* ---------------- Generic Buttons ---------------- */
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div { border-radius: 8px !important; }
    .stButton > button {
        border-radius: 8px; font-weight: 700; border: none;
        background: var(--primary-gradient); color: white; height: 42px; transition: all 0.2s ease;
    }
    .stButton > button:hover { opacity: 0.92; transform: translateY(-1px); }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# DATA HELPERS
# =========================================================
def load_profile_summary():
    try:
        with open("data/profile.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


profile = load_profile_summary()
weak_count = len(get_weak_topics())
notes_count = len(list_notes())
jobs_count = len(list_job_descriptions())
skills_count = len(profile.get("skills", []))
user_name = profile.get("name", "there")
career_goal = profile.get("career_goal", "Not set")
target_roles = profile.get("target_roles", [])

NAV_ITEMS = ["Overview", "Ask PathPilot", "StudyPilot", "CareerPilot", "SkillGap Engine", "Weak Topics", "Profile Settings"]

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown(
        f"""
        <div class="brand">
            <div class="brand-logo">{icon("sparkle", 20, "white")}</div>
            <div>
                <div class="brand-title">PathPilot AI</div>
                <div class="brand-subtitle">Personal Growth Copilot</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="nav-label">NAVIGATION</div>', unsafe_allow_html=True)

    if "active_page" not in st.session_state:
        st.session_state.active_page = "Overview"

    nav_items = [
        ("⌂", "Overview"),
        ("✦", "Ask PathPilot"),
        ("▤", "StudyPilot"),
        ("▣", "CareerPilot"),
        ("◇", "SkillGap Engine"),
        ("△", "Weak Topics"),
    ]

    for nav_icon, item in nav_items:
        wrap_class = "nav-btn-active" if st.session_state.active_page == item else "nav-btn-wrap"
        st.markdown(f'<div class="{wrap_class}">', unsafe_allow_html=True)
        if st.button(
            f"{nav_icon}    {item}",
            key=f"nav_{item}",
            type="primary" if st.session_state.active_page == item else "secondary",
            use_container_width=True,
        ):
            st.session_state.active_page = item
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="nav-divider"></div>', unsafe_allow_html=True)

    wrap_class = "nav-btn-active" if st.session_state.active_page == "Profile Settings" else "nav-btn-wrap"
    st.markdown(f'<div class="{wrap_class}">', unsafe_allow_html=True)
    if st.button(
        "⚙    Profile Settings",
        key="nav_Profile_Settings",
        type="primary" if st.session_state.active_page == "Profile Settings" else "secondary",
        use_container_width=True,
    ):
        st.session_state.active_page = "Profile Settings"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    page = st.session_state.active_page

    st.markdown(
        f"""
        <div class="sidebar-user">
            <div class="sidebar-user-avatar">{icon("user", 18)}</div>
            <div>
                <div style="font-weight: 700; font-size: 0.85rem;">{user_name}</div>
                <div style="color: #64748B; font-size: 0.72rem;">{career_goal}</div>
            </div>
        </div>
        <div class="sidebar-footer">PathPilot AI<br>Python · Streamlit · Gemini</div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# PAGE: OVERVIEW
# =========================================================
if page == "Overview":
    st.markdown(f'<div class="page-heading">Welcome back, {user_name}</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subheading">Your personal study, skill, and career workspace.</div>', unsafe_allow_html=True)

    # ---- Integrated Hero Card & Search Box ----
    st.markdown(
        f"""
        <div style="position:relative; overflow:hidden; background: linear-gradient(135deg, #0B4A44 0%, #0F766E 55%, #0D9488 100%);
                    border-radius: 16px; padding: 1.9rem 1.9rem 1.3rem 1.9rem; color: white;
                    box-shadow: 0 10px 25px -5px rgba(15, 118, 110, 0.32); margin-bottom: 1rem;">
            <svg width="220" height="220" viewBox="0 0 220 220" style="position:absolute; top:-40px; right:-30px; opacity:0.18;">
                <path d="M10 190 C 70 190, 40 90, 110 90 S 150 10, 210 10" stroke="#FFFFFF" stroke-width="3" fill="none" stroke-dasharray="2 10" stroke-linecap="round"/>
                <circle cx="10" cy="190" r="5" fill="#FFFFFF"/>
                <circle cx="210" cy="10" r="5" fill="#FFFFFF"/>
            </svg>
            <div style="position:relative; display:flex; align-items:center; gap:6px; font-size:0.7rem; font-weight:700; color:#BFE3DE; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.5rem;">
                {icon("compass", 12, "#BFE3DE")} PATHPILOT INTELLIGENCE
            </div>
            <div style="position:relative; font-family:'Poppins',sans-serif; font-size: 1.35rem; font-weight: 700; margin-bottom: 0.3rem; letter-spacing:-0.01em;">What would you like to work on today?</div>
            <div style="position:relative; color: #BFE3DE; font-size: 0.85rem; margin-bottom: 1.1rem;">Get personalized guidance based on your goals, skills, notes, and progress.</div>
        """,
        unsafe_allow_html=True,
    )

    with st.form(key="hero_chat_form", clear_on_submit=True):
        col_in, col_btn = st.columns([5, 1])
        with col_in:
            hero_input = st.text_input(
                "Prompt",
                placeholder="Ask PathPilot about your roadmap, studies, or career...",
                label_visibility="collapsed",
            )
        with col_btn:
            hero_submit = st.form_submit_button(label="Ask Pilot")

    st.markdown("</div>", unsafe_allow_html=True)

    if hero_submit and hero_input.strip():
        st.session_state.messages.append({"role": "user", "content": hero_input})
        with st.spinner("PathPilot is thinking..."):
            response = ask_pathpilot(hero_input)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

    # ---- Chat History ----
    if st.session_state.messages:
        st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-user"><span>You: {msg["content"]}</span></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-ai">{msg["content"]}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ---- Stats Grid ----
    stat_cols = st.columns(4)
    stats = [
        ("target", skills_count, "Skills Tracked"),
        ("book", notes_count, "Study Notes"),
        ("briefcase", jobs_count, "Opportunities"),
        ("alert", weak_count, "Weak Topics"),
    ]
    for col, (ic, num, label) in zip(stat_cols, stats):
        with col:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div>{icon(ic, 18, "#0D9488")}</div>
                    <div class="stat-number">{num}</div>
                    <div class="stat-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:1.6rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Your Workspace</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Tools designed around your learning and career goals.</div>', unsafe_allow_html=True)

    features = [
        ("book", "StudyPilot", "Turn your own notes into explanations and short quizzes."),
        ("briefcase", "CareerPilot", "Analyze how your profile matches internships and job opportunities."),
        ("compass", "SkillGap Engine", "Compare skills and identify which one deserves your attention next."),
        ("alert", "Weak Topics", "Track mistakes and focus your revision where it matters most."),
    ]
    feat_col1, feat_col2 = st.columns(2)
    for i, (ic, title, text) in enumerate(features):
        target_col = feat_col1 if i % 2 == 0 else feat_col2
        with target_col:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-icon">{icon(ic, 17)}</div>
                    <div class="feature-title">{title}</div>
                    <div class="feature-text">{text}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# =========================================================
# PAGE: ASK PATHPILOT
# =========================================================
elif page == "Ask PathPilot":
    st.markdown('<div class="page-heading">Ask PathPilot</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subheading">Your personal AI assistant for study, skills and career decisions.</div>', unsafe_allow_html=True)

    question = st.text_area("Your question", placeholder="e.g. What should I focus on this week?", height=130, label_visibility="collapsed")

    if st.button("Ask PathPilot"):
        if question.strip():
            with st.spinner("PathPilot is thinking..."):
                answer = ask_pathpilot(question)
            st.markdown(f'<div class="answer-box"><div class="answer-label">{icon("sparkle", 14)} PathPilot</div>{answer}</div>', unsafe_allow_html=True)
        else:
            st.warning("Please type a question first.")


# =========================================================
# PAGE: STUDYPILOT
# =========================================================
elif page == "StudyPilot":
    st.markdown('<div class="page-heading">StudyPilot</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subheading">Learn from your own uploaded notes with AI.</div>', unsafe_allow_html=True)

    notes = list_notes()
    if not notes:
        st.info("No notes found. Add a .txt or .md file to `data/notes/`.")
    else:
        selected_note = st.selectbox("Select a study note", notes)
        with st.container(border=True):
            tab1, tab2 = st.tabs(["Ask a Question", "Generate Quiz"])

            with tab1:
                question = st.text_area("Question about this note", placeholder="What do you want to understand from this material?", height=100)
                if st.button("Get AI Answer"):
                    if question.strip():
                        note_content = load_note(selected_note)
                        with st.spinner("PathPilot is thinking..."):
                            answer = ask_pathpilot_with_notes(question, note_content)
                        st.markdown(f'<div class="answer-box"><div class="answer-label">{icon("book", 14)} StudyPilot</div>{answer}</div>', unsafe_allow_html=True)
                    else:
                        st.warning("Please type a question first.")

            with tab2:
                st.markdown("Generate three short questions to test your understanding.")
                if st.button("Generate Quiz"):
                    note_content = load_note(selected_note)
                    quiz_question = "Generate 3 short quiz questions (with answers) based on this material to test my understanding."
                    with st.spinner("Generating quiz..."):
                        quiz = ask_pathpilot_with_notes(quiz_question, note_content)
                    st.markdown(f'<div class="answer-box"><div class="answer-label">{icon("book", 14)} Your AI Quiz</div>{quiz}</div>', unsafe_allow_html=True)


# =========================================================
# PAGE: CAREERPILOT
# =========================================================
elif page == "CareerPilot":
    st.markdown('<div class="page-heading">CareerPilot</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subheading">See how your profile matches an internship or job opportunity.</div>', unsafe_allow_html=True)

    jobs = list_job_descriptions()
    if not jobs:
        st.info("No job descriptions found. Add a .txt file to `data/career/`.")
    else:
        selected_job = st.selectbox("Select an opportunity", jobs)
        if st.button("Analyze Match"):
            job_desc = load_job_description(selected_job)
            with st.spinner("Analyzing this opportunity..."):
                result = ask_pathpilot_career(job_desc)
            st.markdown(f'<div class="answer-box"><div class="answer-label">{icon("briefcase", 14)} CareerPilot Analysis</div>{result}</div>', unsafe_allow_html=True)


# =========================================================
# PAGE: SKILLGAP ENGINE
# =========================================================
elif page == "SkillGap Engine":
    st.markdown('<div class="page-heading">SkillGap Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subheading">Compare two skills and get a personalized priority recommendation.</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="card">
            <div class="eyebrow">DECISION SUPPORT</div>
            <div class="section-title">What should you learn next?</div>
            <div class="section-subtitle">Enter two skills and let PathPilot compare them against your profile.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        skill_a = st.text_input("Option A", placeholder="e.g. React")
    with col2:
        skill_b = st.text_input("Option B", placeholder="e.g. Machine Learning")

    if st.button("Compare & Recommend"):
        if skill_a.strip() and skill_b.strip():
            with st.spinner("Comparing your options..."):
                result = ask_pathpilot_skillgap([skill_a, skill_b])
            st.markdown(f'<div class="answer-box"><div class="answer-label">{icon("compass", 14)} SkillGap Recommendation</div>{result}</div>', unsafe_allow_html=True)
        else:
            st.warning("Please fill in both skill options.")


# =========================================================
# PAGE: WEAK TOPICS
# =========================================================
elif page == "Weak Topics":
    st.markdown('<div class="page-heading">Weak Topics</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subheading">Concepts flagged from quizzes and self-reported mistakes.</div>', unsafe_allow_html=True)

    topics = get_weak_topics()
    if not topics:
        st.info("No weak topics recorded yet. Log one below to get started.")
    else:
        for t in topics:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{t['topic']} — {t['concept']}**")
                    st.markdown(
                        f'<span class="badge badge-warn">Attempts: {t["attempts"]}</span>'
                        f'<span class="badge badge-info">Correct: {t["correct"]}</span>',
                        unsafe_allow_html=True,
                    )
                    st.caption(f"Last reviewed: {t['last_reviewed']}")
                with col2:
                    if st.button("Mark Improved", key=f"{t['topic']}_{t['concept']}"):
                        mark_as_improved(t["topic"], t["concept"])
                        st.rerun()

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(
            """
            <div class="eyebrow">MISTAKE TRACKING</div>
            <div class="section-title">Log a New Mistake</div>
            <div class="section-subtitle">Add a topic and concept so PathPilot can track what needs more practice.</div>
            """,
            unsafe_allow_html=True,
        )

        m_col1, m_col2 = st.columns(2)
        with m_col1:
            new_topic = st.text_input("Topic", key="new_topic", placeholder="e.g. Data Structures")
        with m_col2:
            new_concept = st.text_input("Concept", key="new_concept", placeholder="e.g. BFS")

        if st.button("Record Mistake"):
            if new_topic.strip() and new_concept.strip():
                result = record_mistake(new_topic, new_concept)
                st.success(result)
                st.rerun()
            else:
                st.warning("Please fill in both fields.")


# =========================================================
# PAGE: PROFILE SETTINGS
# =========================================================
elif page == "Profile Settings":
    st.markdown('<div class="page-heading">Profile Settings</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subheading">Manage your profile so PathPilot can personalize its recommendations.</div>', unsafe_allow_html=True)

    current_profile = load_profile_summary()
    with st.container(border=True):
        name = st.text_input("Name", value=current_profile.get("name", ""))
        education = st.text_input("Education", value=current_profile.get("education", ""))
        semester = st.text_input("Semester / Year", value=current_profile.get("semester", ""))
        career_goal_input = st.text_input("Career Goal", value=current_profile.get("career_goal", ""))
        study_time = st.text_input("Available Study Time Per Day", value=current_profile.get("available_study_time_per_day", ""))

        st.markdown("##### Skills")
        skills_text = st.text_area("One skill per line", value="\n".join(current_profile.get("skills", [])), height=120, label_visibility="collapsed")

        st.markdown("##### Projects")
        projects_text = st.text_area("One project per line", value="\n".join(current_profile.get("projects", [])), height=120, label_visibility="collapsed")

        st.markdown("##### Certifications")
        certs_text = st.text_area("One certification per line", value="\n".join(current_profile.get("certifications", [])), height=90, label_visibility="collapsed")

        st.markdown("##### Target Roles")
        roles_text = st.text_area("One role per line", value="\n".join(current_profile.get("target_roles", [])), height=90, label_visibility="collapsed")

        if st.button("Save Changes"):
            updated_profile = {
                "name": name,
                "education": education,
                "semester": semester,
                "skills": [s.strip() for s in skills_text.split("\n") if s.strip()],
                "projects": [p.strip() for p in projects_text.split("\n") if p.strip()],
                "certifications": [c.strip() for c in certs_text.split("\n") if c.strip()],
                "career_goal": career_goal_input,
                "target_roles": [r.strip() for r in roles_text.split("\n") if r.strip()],
                "available_study_time_per_day": study_time,
            }
            with open("data/profile.json", "w", encoding="utf-8") as f:
                json.dump(updated_profile, f, indent=2)
            st.success("Profile updated successfully!")
            st.rerun()