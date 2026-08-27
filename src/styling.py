"""
Comprehensive Luxury Pastel Theme Design System for AI Study Buddy
Engineered with warm pastel mesh canvas, glassmorphic cards, soothing color accents, and crisp modern typography.
"""

import json

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

/* ==========================================================================
   GLOBAL APP & LUMINOUS SOOTHING CANVAS
   ========================================================================== */
html {
    font-size: 16.5px !important;
}

html, body, [class*="css"], .stApp, 
div[data-testid="stAppViewContainer"],
div[data-testid="stHeader"],
div[data-testid="stToolbar"],
div[data-testid="stBottom"] {
    background-color: #f8fafd !important;
    background: 
        radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.06) 0px, transparent 50%),
        radial-gradient(at 100% 0%, rgba(14, 165, 233, 0.05) 0px, transparent 50%),
        radial-gradient(at 50% 100%, rgba(16, 185, 129, 0.04) 0px, transparent 50%),
        linear-gradient(135deg, #f8fafc 0%, #f1f5f9 30%, #f3f6fc 60%, #f0fdf9 100%) !important;
    background-attachment: fixed !important;
    color: #1e293b !important;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

/* Breathable Block Container */
.main .block-container {
    max-width: 1260px !important;
    padding-top: 1.25rem !important;
    padding-bottom: 3.5rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

/* Completely Hide Streamlit Header, Deploy Button, Menu and Footer */
#MainMenu { visibility: hidden !important; display: none !important; }
header { visibility: hidden !important; height: 0 !important; display: none !important; }
footer { visibility: hidden !important; display: none !important; }
div[data-testid="stToolbar"] { visibility: hidden !important; display: none !important; }
div[data-testid="stDecoration"] { visibility: hidden !important; display: none !important; }
div[data-testid="stStatusWidget"] { visibility: hidden !important; display: none !important; }
.stDeployButton { visibility: hidden !important; display: none !important; }
button[title="View app in Streamlit Community Cloud"] { visibility: hidden !important; display: none !important; }
div[data-testid="stHeader"] { visibility: hidden !important; display: none !important; height: 0 !important; }
div[data-testid="stMainMenu"] { visibility: hidden !important; display: none !important; }
button[kind="header"] { visibility: hidden !important; display: none !important; }

/* Completely Hide Sidebar and Sidebar Toggles */
section[data-testid="stSidebar"],
div[data-testid="stSidebar"],
button[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"] {
    display: none !important;
}

/* Compact Knowledge Stats Row */
.sidebar-stats-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 0.85rem;
}

.sidebar-stat-box {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 0.75rem 0.85rem;
    text-align: center;
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.03);
}

.sidebar-stat-number {
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.45rem;
    font-weight: 800;
    color: #4f46e5;
    line-height: 1.15;
}

.sidebar-stat-label {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #64748b;
    margin-top: 3px;
}

/* File Uploader styling */
[data-testid="stFileUploader"] {
    padding: 0 !important;
}

[data-testid="stFileUploader"] > div:first-child {
    background: #ffffff !important;
    border: 1.5px dashed #cbd5e1 !important;
    border-radius: 12px !important;
    padding: 0.85rem !important;
    font-size: 0.95rem !important;
}

[data-testid="stFileUploader"] > div:first-child:hover {
    border-color: #4f46e5 !important;
    background: #f5f3ff !important;
}

/* Typography Headings */
h1, h2, h3, h4, h5, h6,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5 {
    font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif !important;
    color: #0f172a !important;
    font-weight: 700 !important;
    letter-spacing: -0.025em !important;
}

h1, .stMarkdown h1 {
    font-size: 2.35rem !important;
}

h2, .stMarkdown h2 {
    font-size: 1.85rem !important;
}

h3, .stMarkdown h3 {
    font-size: 1.45rem !important;
}

h4, .stMarkdown h4 {
    font-size: 1.2rem !important;
}

h5, .stMarkdown h5 {
    font-size: 1.08rem !important;
}

p, span, label, li,
.stMarkdown p, .stMarkdown li, .stMarkdown span {
    color: #334155 !important;
    font-size: 0.98rem !important;
    line-height: 1.65 !important;
}

/* Streamlit Tabs Typography */
button[data-baseweb="tab"] div,
button[data-baseweb="tab"] p {
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.02rem !important;
    font-weight: 600 !important;
    letter-spacing: -0.01em !important;
}

/* Primary and Secondary Buttons */
div.stButton > button,
button[kind="primary"],
button[kind="secondary"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.96rem !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
}

/* ==========================================================================
   LANDING PAGE STYLING
   ========================================================================== */
.hero-container {
    background: rgba(255, 255, 255, 0.92);
    backdrop-filter: blur(20px);
    border: 1.5px solid rgba(226, 232, 240, 0.9);
    border-radius: 20px;
    padding: clamp(1.25rem, 4vw, 2.75rem) clamp(1rem, 3vw, 2.25rem);
    text-align: center;
    margin-bottom: 1.75rem;
    box-shadow: 0 20px 40px -15px rgba(30, 41, 59, 0.05), 0 4px 12px -2px rgba(30, 41, 59, 0.02);
}

.hero-pill-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: linear-gradient(135deg, #eef2ff 0%, #f5f3ff 100%);
    color: #4f46e5;
    border: 1px solid #c7d2fe;
    padding: 0.35rem 0.95rem;
    border-radius: 999px;
    font-size: clamp(0.76rem, 2vw, 0.88rem);
    font-weight: 700;
    margin-bottom: 0.95rem;
    box-shadow: 0 2px 6px rgba(99, 102, 241, 0.08);
}

.hero-h1 {
    font-family: 'Outfit', sans-serif !important;
    font-size: clamp(1.75rem, 5.5vw, 2.75rem) !important;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.035em;
    line-height: 1.2;
    margin-bottom: 0.75rem;
}

.hero-h1-gradient {
    background: linear-gradient(135deg, #4338ca 0%, #3b82f6 50%, #06b6d4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtext {
    font-size: clamp(0.92rem, 2.5vw, 1.12rem);
    color: #475569;
    max-width: 800px;
    margin: 0 auto 1.45rem auto;
    line-height: 1.65;
}

.feature-card {
    background: rgba(255, 255, 255, 0.94);
    backdrop-filter: blur(16px);
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 1.5rem;
    box-shadow: 0 4px 20px -4px rgba(30, 41, 59, 0.04);
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    height: 100%;
}

.feature-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 28px -6px rgba(79, 70, 229, 0.12);
    border-color: #c7d2fe;
}

.feature-icon-wrapper {
    width: 50px;
    height: 50px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    margin-bottom: 1rem;
}

.feature-title {
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.15rem;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 0.45rem;
}

.feature-desc {
    font-size: 0.92rem;
    color: #64748b;
    line-height: 1.6;
}

.step-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 1.45rem 1.25rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
    height: 100%;
}

.step-num {
    display: inline-block;
    width: 34px;
    height: 34px;
    line-height: 34px;
    border-radius: 50%;
    background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
    color: #ffffff;
    font-size: 0.9rem;
    font-weight: 700;
    margin-bottom: 0.65rem;
    box-shadow: 0 2px 8px rgba(79, 70, 229, 0.25);
}

/* ==========================================================================
   UNIFIED TOP NAV BAR (FROSTED GLASSMORPHISM)
   ========================================================================== */
.top-nav-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(255, 255, 255, 0.94);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(226, 232, 240, 0.9);
    border-radius: 16px;
    padding: 0.7rem 1.35rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 4px 20px -4px rgba(30, 41, 59, 0.05);
    flex-wrap: wrap;
    gap: 0.75rem;
    min-height: 54px;
}

.nav-back-link {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #f5f3ff;
    color: #4f46e5 !important;
    border: 1.5px solid #ddd6fe;
    padding: 0.38rem 0.9rem;
    border-radius: 10px;
    font-size: 0.82rem;
    font-weight: 700;
    text-decoration: none !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-back-link:hover {
    background: #ede9fe;
    border-color: #c4b5fd;
    color: #3730a3 !important;
    transform: translateX(-2px);
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.15);
}

.nav-divider {
    color: #cbd5e1;
    font-weight: 300;
    font-size: 1.1rem;
    margin: 0 0.15rem;
}

.brand-section {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.brand-title {
    font-size: 1.35rem;
    font-weight: 800;
    color: #4338ca;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    letter-spacing: -0.02em;
}

.brand-tag {
    background: #f5f3ff;
    color: #6366f1;
    border: 1px solid #ddd6fe;
    padding: 0.2rem 0.55rem;
    border-radius: 6px;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
}

.user-stats-section {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    flex-wrap: wrap;
}

.stat-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.3rem 0.7rem;
    border-radius: 10px;
    font-size: 0.78rem;
    font-weight: 600;
}

.stat-pill-xp {
    background: #faf5ff;
    color: #7e22ce;
    border: 1px solid #e9d5ff;
}

.stat-pill-streak {
    background: #fffbeb;
    color: #b45309;
    border: 1px solid #fde68a;
}

.stat-pill-quote {
    background: #f0fdf4;
    color: #15803d;
    border: 1px solid #bbf7d0;
    max-width: 320px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* ==========================================================================
   NAVIGATION TABS (CLEAN MODERN UNDERLINE)
   ========================================================================== */
.stTabs {
    margin-top: 0.5rem !important;
}

.stTabs [data-baseweb="tab-list"] {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 1.75rem !important;
    background: transparent !important;
    border-bottom: 1px solid #ede8e3 !important;
    padding: 0 0 2px 0 !important;
    margin-bottom: 1.75rem !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    background-color: #4f46e5 !important;
    height: 2.5px !important;
    border-radius: 999px !important;
}

.stTabs [data-baseweb="tab-border"] {
    display: none !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    color: #64748b !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 0.25rem !important;
    white-space: nowrap !important;
    transition: color 0.15s ease !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    height: auto !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #0f172a !important;
    background: transparent !important;
}

.stTabs [aria-selected="true"] {
    background: transparent !important;
    color: #4f46e5 !important;
    font-weight: 700 !important;
    box-shadow: none !important;
}

.stTabs [aria-selected="true"] * {
    color: #4f46e5 !important;
}

/* ==========================================================================
   CARD CONTAINERS & GLASSMORPHIC BLOCKS
   ========================================================================== */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 0.92) !important;
    backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(226, 232, 240, 0.88) !important;
    border-radius: 18px !important;
    box-shadow: 0 10px 30px -4px rgba(15, 23, 42, 0.05), 0 2px 6px -1px rgba(15, 23, 42, 0.02) !important;
    padding: 1.5rem !important;
    margin-bottom: 1.25rem !important;
}

/* Quick prompt chips */
.chip-btn {
    display: inline-flex;
    align-items: center;
    padding: 0.45rem 0.95rem;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 600;
    color: #334155;
    cursor: pointer;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.chip-btn:hover {
    background: #f0f4ff;
    color: #4338ca;
    border-color: #c7d2fe;
    transform: translateY(-1.5px);
    box-shadow: 0 4px 10px rgba(99, 102, 241, 0.12);
}

/* Buttons */
.stButton > button,
div[data-testid="stFormSubmitButton"] > button,
button[data-testid="baseButton-secondary"] {
    background: #ffffff !important;
    color: #1e293b !important;
    font-weight: 600 !important;
    border: 1.5px solid #cbd5e1 !important;
    border-radius: 10px !important;
    padding: 0.55rem 1.25rem !important;
    box-shadow: 0 2px 5px rgba(15, 23, 42, 0.03) !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.stButton > button:hover {
    background: #f8fafc !important;
    border-color: #94a3b8 !important;
    color: #0f172a !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.06) !important;
}

/* Primary and Form Submit Buttons */
.stButton > button[kind="primary"],
div[data-testid="stFormSubmitButton"] > button,
div[data-testid="stFormSubmitButton"] > button[kind="primary"],
button[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%) !important;
    border: 1px solid #4338ca !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    box-shadow: 0 4px 16px rgba(79, 70, 229, 0.35) !important;
    cursor: pointer !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.stButton > button[kind="primary"] *,
div[data-testid="stFormSubmitButton"] > button *,
div[data-testid="stFormSubmitButton"] button p,
div[data-testid="stFormSubmitButton"] button span,
button[data-testid="baseButton-primary"] * {
    color: #ffffff !important;
    font-weight: 700 !important;
}

.stButton > button[kind="primary"]:hover,
div[data-testid="stFormSubmitButton"] > button:hover {
    background: linear-gradient(135deg, #4338ca 0%, #2563eb 100%) !important;
    border-color: #3730a3 !important;
    color: #ffffff !important;
    box-shadow: 0 8px 24px rgba(79, 70, 229, 0.45) !important;
    transform: translateY(-2px) !important;
}

/* Text Inputs & Select Boxes */
div[data-baseweb="input"],
div[data-baseweb="select"] > div,
div[data-baseweb="textarea"] {
    background-color: #ffffff !important;
    border: 1.5px solid #cbd5e1 !important;
    border-radius: 11px !important;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03) !important;
    transition: all 0.2s ease !important;
}

div[data-baseweb="input"]:focus-within,
div[data-baseweb="select"] > div:focus-within,
div[data-baseweb="textarea"]:focus-within {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3.5px rgba(99, 102, 241, 0.18) !important;
}

/* Completely Hide Streamlit "Press Ctrl+Enter to apply" helper text */
div[data-testid="InputInstructions"],
div[data-testid="stTextArea"] [data-testid="InputInstructions"],
div[data-testid="stTextInput"] [data-testid="InputInstructions"],
.stTextArea [data-testid="InputInstructions"],
div[data-baseweb="textarea"] + div,
div[data-baseweb="textarea"] ~ div,
span[data-testid="stWidgetInstructions"],
[data-testid="stWidgetInstructions"] {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    opacity: 0 !important;
}

/* Chat Messages */
div[data-testid="stChatMessage"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 16px !important;
    padding: 1.25rem !important;
    margin-bottom: 0.95rem !important;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.03) !important;
}

div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
    background: linear-gradient(135deg, #f0f4ff 0%, #f5f3ff 100%) !important;
    border-color: #c7d2fe !important;
}

/* Direct Click-to-Edit User Chat Bubble */
div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) div[data-baseweb="input"] {
    background: transparent !important;
    border: 1px solid transparent !important;
    box-shadow: none !important;
    cursor: text !important;
    padding: 0 !important;
}

div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) div[data-baseweb="input"]:hover {
    border: 1px dashed #cbd5e1 !important;
    background: #ffffff !important;
    border-radius: 8px !important;
}

div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) div[data-baseweb="input"]:focus-within {
    border: 1.5px solid #6366f1 !important;
    background: #ffffff !important;
    border-radius: 8px !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
}

div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) input {
    font-size: 0.98rem !important;
    font-weight: 600 !important;
    color: #0f172a !important;
    cursor: text !important;
}

/* Interactive Daily Subtopic Checkboxes */
div[data-testid="stCheckbox"]:has(input[id*="chk_task_"]) {
    background: #ffffff !important;
    border: 1px solid #ede8e3 !important;
    border-left: 3.5px solid #6366f1 !important;
    border-radius: 9px !important;
    padding: 0.5rem 0.85rem !important;
    margin-bottom: 0.45rem !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02) !important;
    transition: all 0.2s ease !important;
}

div[data-testid="stCheckbox"]:has(input[id*="chk_task_"]):hover {
    border-color: #cbd5e1 !important;
    background: #f8fafc !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04) !important;
}

div[data-testid="stCheckbox"]:has(input[id*="chk_task_"]:checked) {
    background: #f0fdf4 !important;
    border-color: #bbf7d0 !important;
    border-left: 3.5px solid #10b981 !important;
}

div[data-testid="stCheckbox"]:has(input[id*="chk_task_"]:checked) label span p {
    text-decoration: line-through !important;
    color: #64748b !important;
}

/* ==========================================================================
   KAHOOT QUIZ ARENA LUXURY STYLING
   ========================================================================== */
.kahoot-card {
    background: #ffffff;
    border: 1px solid #ede8e3;
    border-radius: 16px;
    padding: 1.35rem 1.5rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.03);
}

.kahoot-q-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #f5f3ff;
    color: #4f46e5;
    border: 1px solid #ddd6fe;
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 700;
    margin-bottom: 0.65rem;
}

.kahoot-question-title {
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.18rem;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.45;
}

/* ==========================================================================
   INTERACTIVE RESOURCE TILES & POPOVER STYLING
   ========================================================================== */
.popover-header {
    background: #fdfbf7;
    border: 1px solid #ede8e3;
    border-radius: 8px;
    padding: 0.5rem 0.75rem;
    margin-bottom: 0.75rem;
    font-size: 0.85rem;
    font-weight: 700;
    color: #1e293b;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

.resource-tile-list {
    display: flex;
    flex-direction: column;
    gap: 6px;
    margin-bottom: 0.5rem;
}

.resource-tile {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.55rem 0.85rem;
    border-radius: 8px;
    text-decoration: none !important;
    font-size: 0.82rem;
    font-weight: 600;
    transition: all 0.15s ease;
    border: 1px solid transparent;
    cursor: pointer;
}

.resource-tile:hover {
    transform: translateY(-1px);
    text-decoration: none !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.resource-tile-blue {
    background: #eff6ff;
    color: #1d4ed8 !important;
    border-color: #bfdbfe;
}
.resource-tile-blue:hover {
    background: #dbeafe;
    color: #1e40af !important;
}

.resource-tile-green {
    background: #ecfdf5;
    color: #047857 !important;
    border-color: #a7f3d0;
}
.resource-tile-green:hover {
    background: #d1fae5;
    color: #065f46 !important;
}

.resource-tile-red {
    background: #fff1f2;
    color: #be123c !important;
    border-color: #fecdd3;
}
.resource-tile-red:hover {
    background: #ffe4e6;
    color: #9f1239 !important;
}

.resource-tile-amber {
    background: #fffbeb;
    color: #b45309 !important;
    border-color: #fde68a;
}
.resource-tile-amber:hover {
    background: #fef3c7;
    color: #92400e !important;
}

.resource-tile-purple {
    background: #faf5ff;
    color: #7e22ce !important;
    border-color: #e9d5ff;
}
.resource-tile-purple:hover {
    background: #f3e8ff;
    color: #6b21a8 !important;
}

.subtopics-label {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #64748b;
    margin: 0.6rem 0 0.35rem 0;
}

div[data-testid="stAlert"] {
    border-radius: 10px !important;
}

/* ==========================================================================
   MODERN SCROLLBARS & EXPANDERS
   ========================================================================== */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 999px;
}

::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
}

div[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid #ede8e3 !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02) !important;
    margin-bottom: 0.75rem !important;
}

details[data-testid="stExpander"] summary {
    font-weight: 600 !important;
    color: #334155 !important;
}

details[data-testid="stExpander"] summary:hover {
    color: #4f46e5 !important;
}

/* ==========================================================================
   COMPREHENSIVE RESPONSIVE MEDIA QUERIES (ALL SCREEN SIZES)
   ========================================================================== */

/* Tablets & Small Laptops (max-width: 992px) */
@media screen and (max-width: 992px) {
    .main .block-container {
        padding-left: 1.25rem !important;
        padding-right: 1.25rem !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 1.15rem !important;
    }
    .stat-pill-quote {
        max-width: 220px !important;
    }
}

/* Mobile Devices & Tablets (max-width: 768px) */
@media screen and (max-width: 768px) {
    html {
        font-size: 15px !important;
    }
    .main .block-container {
        padding-top: 0.75rem !important;
        padding-bottom: 2rem !important;
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
    }
    .top-nav-bar {
        flex-direction: column !important;
        align-items: stretch !important;
        gap: 0.65rem !important;
        padding: 0.85rem 1rem !important;
        margin-bottom: 1.25rem !important;
    }
    .brand-section {
        justify-content: flex-start !important;
        flex-wrap: wrap !important;
        gap: 0.4rem !important;
    }
    .user-stats-section {
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 6px !important;
        width: 100% !important;
    }
    .stat-pill {
        flex-grow: 1 !important;
        justify-content: center !important;
        font-size: 0.74rem !important;
        padding: 0.25rem 0.5rem !important;
    }
    .stat-pill-quote {
        flex-basis: 100% !important;
        max-width: 100% !important;
        text-align: center !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        overflow-x: auto !important;
        flex-wrap: nowrap !important;
        gap: 0.85rem !important;
        -webkit-overflow-scrolling: touch !important;
        padding-bottom: 8px !important;
        margin-bottom: 1.15rem !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 0.88rem !important;
        padding: 0.45rem 0.15rem !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        padding: 1rem !important;
        border-radius: 12px !important;
        margin-bottom: 1rem !important;
    }
    .kahoot-card {
        padding: 1rem !important;
        border-radius: 12px !important;
    }
    .kahoot-question-title {
        font-size: 1.05rem !important;
    }
    .sidebar-stats-row {
        gap: 6px !important;
    }
    .sidebar-stat-number {
        font-size: 1.25rem !important;
    }
}

/* Small Smart Phones (max-width: 480px) */
@media screen and (max-width: 480px) {
    html {
        font-size: 14px !important;
    }
    .main .block-container {
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }
    .top-nav-bar {
        padding: 0.75rem 0.75rem !important;
        border-radius: 12px !important;
    }
    .brand-title {
        font-size: 1.05rem !important;
    }
    .nav-back-link {
        font-size: 0.72rem !important;
        padding: 0.2rem 0.45rem !important;
    }
    .stat-pill-quote {
        display: none !important;
    }
    .stat-pill {
        font-size: 0.7rem !important;
        padding: 0.2rem 0.4rem !important;
    }
    .stButton > button,
    div[data-testid="stFormSubmitButton"] > button {
        padding: 0.5rem 0.85rem !important;
        font-size: 0.88rem !important;
    }
    div[data-testid="stChatMessage"] {
        padding: 0.85rem !important;
        border-radius: 10px !important;
    }
}
</style>
"""

def render_top_nav(lvl_info, student_xp, streak, daily_quote=None, show_back=False):
    """Renders the sleek, uncluttered top navigation bar with XP and Streak metrics."""
    back_html = '<a href="/?page=homepage" target="_self" class="nav-back-link"><span>⬅️</span><span>Back to Homepage</span></a><span class="nav-divider">|</span>' if show_back else ''

    return (
        '<div class="top-nav-bar">'
        '<div class="brand-section">'
        f'{back_html}'
        '<span class="brand-title">🧠 AI Study Buddy</span>'
        '<span class="brand-tag">Multi-LLM RAG</span>'
        '</div>'
        '<div class="user-stats-section">'
        f'<span class="stat-pill stat-pill-xp">{lvl_info["icon"]} <strong>Level {lvl_info["current_level"]}</strong> ({student_xp} XP)</span>'
        f'<span class="stat-pill stat-pill-streak">🔥 <strong>{streak} Day Streak</strong></span>'
        '</div>'
        '</div>'
    )

def render_motivation_banner(quotes_data):
    """
    Renders a luxury top motivation card that smoothly auto-cycles to a new
    inspirational learning mantra every 10 seconds via client-side timer.
    """
    if isinstance(quotes_data, list) and len(quotes_data) > 0:
        quotes = quotes_data
    elif isinstance(quotes_data, dict):
        quotes = [quotes_data]
    else:
        quotes = [{"quote": "Mastery is the daily accumulation of focused understanding.", "author": "Academic Focus"}]

    first_quote = quotes[0].get("quote", "")
    first_author = quotes[0].get("author", "")
    quotes_json = json.dumps(quotes)

    return (
        f'<div class="daily-mindset-banner" style="background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%); border: 1.5px solid #bbf7d0; border-radius: 12px; padding: 0.75rem 1.25rem; margin-bottom: 1.15rem; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 2px 8px rgba(34, 197, 94, 0.05); gap: 12px; flex-wrap: wrap; position: relative; overflow: hidden;">'
        f'<div id="mindset-content-box" style="display: flex; align-items: center; gap: 10px; font-size: 0.94rem; color: #1e293b; transition: opacity 0.35s ease, transform 0.35s ease;">'
        f'<span style="font-size: 1.3rem;">💡</span>'
        f'<span><strong>Daily Study Mindset:</strong> <em id="mindset-quote-text">"{first_quote}"</em></span>'
        f'</div>'
        f'<div id="mindset-author-badge" style="font-size: 0.76rem; font-weight: 700; color: #15803d; background: #dcfce7; padding: 0.25rem 0.65rem; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.04em; transition: opacity 0.35s ease;">'
        f'{first_author}'
        f'</div>'
        f'<div style="position: absolute; bottom: 0; left: 0; height: 2.5px; background: linear-gradient(90deg, #22c55e, #16a34a); width: 100%; animation: mindsetProgress 10s linear infinite;"></div>'
        f'</div>'
        f'<style>'
        f'@keyframes mindsetProgress {{'
        f'  0% {{ width: 0%; opacity: 0.8; }}'
        f'  95% {{ width: 100%; opacity: 1; }}'
        f'  100% {{ width: 100%; opacity: 0; }}'
        f'}}'
        f'</style>'
        f'<script>'
        f'(function() {{'
        f'  var quotes = {quotes_json};'
        f'  if (!quotes || quotes.length <= 1) return;'
        f'  var curIdx = 0;'
        f'  if (window._study_mindset_timer) {{ clearInterval(window._study_mindset_timer); }}'
        f'  window._study_mindset_timer = setInterval(function() {{'
        f'    curIdx = (curIdx + 1) % quotes.length;'
        f'    var box = document.getElementById("mindset-content-box");'
        f'    var badge = document.getElementById("mindset-author-badge");'
        f'    var txt = document.getElementById("mindset-quote-text");'
        f'    if (box && badge && txt) {{'
        f'      box.style.opacity = "0";'
        f'      box.style.transform = "translateY(-3px)";'
        f'      badge.style.opacity = "0";'
        f'      setTimeout(function() {{'
        f'        txt.textContent = "\\"" + quotes[curIdx].quote + "\\"";'
        f'        badge.textContent = quotes[curIdx].author;'
        f'        box.style.opacity = "1";'
        f'        box.style.transform = "translateY(0)";'
        f'        badge.style.opacity = "1";'
        f'      }}, 350);'
        f'    }}'
        f'  }}, 10000);'
        f'}})();'
        f'</script>'
    )

def render_quiz_results_dashboard(res):
    """Renders a sleek, modern, gamified scorecard for quiz evaluation results."""
    tot_q = res.get("total_questions", len(res.get("breakdown", [])))
    corr_q = res.get("correct_count", 0)
    wrong_q = res.get("wrong_count", max(0, tot_q - corr_q))
    score_p = res.get("score_pct", round(corr_q / tot_q * 100, 1) if tot_q > 0 else 0)
    badge = res.get("badge", "Mastery")
    feedback = res.get("feedback", "Great work on completing the quiz drill!")

    # Performance tier coloring
    if score_p >= 80:
        tier_color = "#16a34a"
        tier_bg = "#f0fdf4"
        tier_border = "#bbf7d0"
        tier_icon = "👑"
    elif score_p >= 50:
        tier_color = "#d97706"
        tier_bg = "#fffbeb"
        tier_border = "#fde68a"
        tier_icon = "⚡"
    else:
        tier_color = "#dc2626"
        tier_bg = "#fef2f2"
        tier_border = "#fecaca"
        tier_icon = "⚠️"

    return (
        f'<div style="background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 18px; padding: 1.35rem 1.5rem; margin: 1.25rem 0; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.04), 0 4px 6px -2px rgba(0, 0, 0, 0.02);">'
        f'<div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #f1f5f9; padding-bottom: 0.85rem; margin-bottom: 1.15rem; flex-wrap: wrap; gap: 10px;">'
        f'<div style="display: flex; align-items: center; gap: 10px;">'
        f'<span style="font-size: 1.4rem;">🏅</span>'
        f'<div>'
        f'<div style="font-family: \'Outfit\', sans-serif; font-size: 1.15rem; font-weight: 800; color: #0f172a;">Quiz Performance Scorecard</div>'
        f'<div style="font-size: 0.8rem; color: #64748b;">Active recall drill evaluated strictly against uploaded syllabus</div>'
        f'</div>'
        f'</div>'
        f'<div style="background: {tier_bg}; border: 1.5px solid {tier_border}; border-radius: 30px; padding: 0.35rem 0.95rem; display: flex; align-items: center; gap: 8px;">'
        f'<span style="font-size: 1.05rem;">{tier_icon}</span>'
        f'<span style="font-weight: 800; font-size: 0.85rem; color: {tier_color}; text-transform: uppercase; letter-spacing: 0.04em;">{badge}</span>'
        f'</div>'
        f'</div>'
        f'<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(105px, 1fr)); gap: 10px; margin-bottom: 1.15rem;">'
        f'<div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 14px; padding: 0.9rem 0.75rem; text-align: center;">'
        f'<div style="font-size: 1.2rem; margin-bottom: 2px;">🎯</div>'
        f'<div style="font-family: \'Outfit\', sans-serif; font-size: 1.6rem; font-weight: 800; color: #3b82f6; line-height: 1.2;">{tot_q}</div>'
        f'<div style="font-size: 0.72rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 3px;">Total Questions</div>'
        f'</div>'
        f'<div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 14px; padding: 0.9rem 0.75rem; text-align: center;">'
        f'<div style="font-size: 1.2rem; margin-bottom: 2px;">✅</div>'
        f'<div style="font-family: \'Outfit\', sans-serif; font-size: 1.6rem; font-weight: 800; color: #16a34a; line-height: 1.2;">{corr_q}</div>'
        f'<div style="font-size: 0.72rem; font-weight: 700; color: #15803d; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 3px;">Correct</div>'
        f'</div>'
        f'<div style="background: #fef2f2; border: 1px solid #fecaca; border-radius: 14px; padding: 0.9rem 0.75rem; text-align: center;">'
        f'<div style="font-size: 1.2rem; margin-bottom: 2px;">❌</div>'
        f'<div style="font-family: \'Outfit\', sans-serif; font-size: 1.6rem; font-weight: 800; color: #dc2626; line-height: 1.2;">{wrong_q}</div>'
        f'<div style="font-size: 0.72rem; font-weight: 700; color: #b91c1c; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 3px;">Incorrect</div>'
        f'</div>'
        f'<div style="background: linear-gradient(135deg, #eff6ff 0%, #e0e7ff 100%); border: 1px solid #bfdbfe; border-radius: 14px; padding: 0.9rem 0.75rem; text-align: center;">'
        f'<div style="font-size: 1.2rem; margin-bottom: 2px;">📈</div>'
        f'<div style="font-family: \'Outfit\', sans-serif; font-size: 1.6rem; font-weight: 800; color: #4f46e5; line-height: 1.2;">{score_p}%</div>'
        f'<div style="font-size: 0.72rem; font-weight: 700; color: #4338ca; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 3px;">Accuracy</div>'
        f'</div>'
        f'</div>'
        f'<div style="background: #f8fafc; border-left: 4px solid {tier_color}; border-radius: 8px; padding: 0.75rem 1.15rem; font-size: 0.9rem; color: #334155; display: flex; align-items: center; gap: 10px;">'
        f'<span>💡</span>'
        f'<span><strong>Tutor Feedback:</strong> {feedback}</span>'
        f'</div>'
        f'</div>'
    )

def render_pomodoro_timer():
    """
    Renders an interactive, client-side Pomodoro Focus Timer with ambient audio synthesizer
    (Rain / Coffee Shop / White Noise) and celebration completion chime.
    """
    return (
        '<style>'
        '@import url("https://fonts.googleapis.com/css2?family=Outfit:wght@600;700;800&family=Plus+Jakarta+Sans:wght@500;600;700&display=swap");'
        '* { box-sizing: border-box; margin: 0; padding: 0; }'
        'html, body { font-family: "Plus Jakarta Sans", sans-serif; background: transparent; padding: 0; margin: 0; width: 100%; }'
        '.pomo-card { background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 16px; padding: 0.85rem 1rem; box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04); }'
        '.pomo-header { display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #f1f5f9; padding-bottom: 0.45rem; margin-bottom: 0.65rem; flex-wrap: wrap; gap: 6px; }'
        '.pomo-grid { display: grid; grid-template-columns: 130px 1fr; gap: 0.85rem; align-items: center; }'
        '@media (max-width: 480px) { .pomo-grid { grid-template-columns: 1fr; justify-items: center; } .pomo-controls-box { width: 100%; } }'
        '.pomo-timer-box { display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; }'
        '.pomo-controls-box { display: flex; flex-direction: column; gap: 0.45rem; width: 100%; }'
        '.pomo-btn-mode { flex: 1; min-width: 65px; background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 8px; padding: 0.35rem 0.35rem; font-size: 0.72rem; font-weight: 700; color: #475569; cursor: pointer; transition: all 0.15s ease; text-align: center; }'
        '.pomo-btn-mode:hover { border-color: #6366f1; color: #4338ca; background: #f8fafc; }'
        '</style>'
        '<div class="pomo-card">'
        '<div class="pomo-header">'
        '<div style="display: flex; align-items: center; gap: 8px;">'
        '<span style="font-size: 1.25rem;">⏱️</span>'
        '<div>'
        '<div style="font-family: \'Outfit\', sans-serif; font-size: 1.05rem; font-weight: 800; color: #0f172a;">Pomodoro Focus Arena</div>'
        '<div style="font-size: 0.72rem; color: #64748b;">Execute targeted study blocks with ambient focus audio</div>'
        '</div>'
        '</div>'
        '<div id="pomo-mode-badge" style="background: #eef2ff; color: #4f46e5; border: 1px solid #c7d2fe; border-radius: 20px; padding: 0.2rem 0.65rem; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.03em;">'
        '🍅 25m Focus'
        '</div>'
        '</div>'
        '<div class="pomo-grid">'
        '<div class="pomo-timer-box">'
        '<svg width="120" height="120" viewBox="0 0 120 120" style="transform: rotate(-90deg);">'
        '<circle cx="60" cy="60" r="50" stroke="#f1f5f9" stroke-width="8" fill="transparent" />'
        '<circle id="pomo-progress-circle" cx="60" cy="60" r="50" stroke="url(#pomoGradient)" stroke-width="8" stroke-linecap="round" fill="transparent" stroke-dasharray="314.16" stroke-dashoffset="0" style="transition: stroke-dashoffset 0.85s linear;" />'
        '<defs>'
        '<linearGradient id="pomoGradient" x1="0%" y1="0%" x2="100%" y2="100%">'
        '<stop offset="0%" stop-color="#4f46e5" />'
        '<stop offset="100%" stop-color="#06b6d4" />'
        '</linearGradient>'
        '</defs>'
        '</svg>'
        '<div style="position: absolute; text-align: center;">'
        '<div id="pomo-timer-display" style="font-family: \'Outfit\', monospace; font-size: 1.55rem; font-weight: 800; color: #0f172a; line-height: 1;">25:00</div>'
        '<div id="pomo-status-label" style="font-size: 0.65rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.04em; margin-top: 2px;">Ready</div>'
        '</div>'
        '</div>'
        '<div class="pomo-controls-box">'
        '<div style="display: flex; gap: 5px; flex-wrap: wrap;">'
        '<button type="button" class="pomo-btn-mode" onclick="setPomodoroMode(25, \'🍅 25m Focus\', \'#4f46e5\', \'#eef2ff\')">🍅 25m Focus</button>'
        '<button type="button" class="pomo-btn-mode" onclick="setPomodoroMode(50, \'⚡ 50m Deep\', \'#7e22ce\', \'#faf5ff\')">⚡ 50m Deep</button>'
        '<button type="button" class="pomo-btn-mode" onclick="setPomodoroMode(5, \'☕ 5m Break\', \'#15803d\', \'#f0fdf4\')">☕ 5m Break</button>'
        '</div>'
        '<div style="display: flex; gap: 6px;">'
        '<button id="pomo-toggle-btn" type="button" onclick="togglePomodoroTimer()" style="flex: 2; background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%); color: #ffffff; border: none; border-radius: 9px; padding: 0.45rem 0.75rem; font-size: 0.84rem; font-weight: 700; cursor: pointer; box-shadow: 0 3px 10px rgba(79, 70, 229, 0.25);">▶️ Start Focus</button>'
        '<button type="button" onclick="resetPomodoroTimer()" style="flex: 1; background: #ffffff; color: #64748b; border: 1.5px solid #cbd5e1; border-radius: 9px; padding: 0.45rem 0.5rem; font-size: 0.8rem; font-weight: 600; cursor: pointer;">🔄 Reset</button>'
        '</div>'
        '<div style="display: flex; align-items: center; justify-content: space-between; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.3rem 0.65rem;">'
        '<span style="font-size: 0.74rem; font-weight: 700; color: #475569;">🎧 Ambient:</span>'
        '<select id="pomo-audio-select" onchange="switchAmbientSound(this.value)" style="font-size: 0.72rem; font-weight: 600; border: 1px solid #cbd5e1; border-radius: 5px; padding: 2px 4px; background: #ffffff; color: #1e293b; outline: none; cursor: pointer;">'
        '<option value="none">🔇 Off (Silent)</option>'
        '<option value="rain">🌧️ Gentle Rain</option>'
        '<option value="cafe">☕ Coffee Shop</option>'
        '<option value="ocean">🌊 Ocean Calm</option>'
        '</select>'
        '</div>'
        '</div>'
        '</div>'
        '<div id="pomo-celebrate-box" style="display: none; margin-top: 0.65rem; background: #f0fdf4; border: 1.5px solid #86efac; border-radius: 8px; padding: 0.45rem 0.75rem; text-align: center; color: #15803d; font-size: 0.82rem; font-weight: 700;">'
        '🎉 Focus block completed! Take a breather.'
        '</div>'
        '</div>'
        '<script>'
        'var totalSec = 25 * 60;'
        'var leftSec = totalSec;'
        'var isRunning = false;'
        'var timerInterval = null;'
        'var audioCtx = null;'
        'var noiseNode = null;'
        'var gainNode = null;'
        ''
        'function setPomodoroMode(mins, label, color, bg) {'
        '  clearInterval(timerInterval);'
        '  isRunning = false;'
        '  totalSec = mins * 60;'
        '  leftSec = totalSec;'
        '  updateDisplay();'
        '  var badge = document.getElementById("pomo-mode-badge");'
        '  var status = document.getElementById("pomo-status-label");'
        '  var btn = document.getElementById("pomo-toggle-btn");'
        '  var cel = document.getElementById("pomo-celebrate-box");'
        '  if (cel) cel.style.display = "none";'
        '  if (badge) { badge.textContent = label; badge.style.color = color; badge.style.background = bg; }'
        '  if (status) { status.textContent = "Ready"; }'
        '  if (btn) { btn.textContent = "▶️ Start " + (mins >= 25 ? "Focus" : "Break"); }'
        '  stopAmbientSound();'
        '};'
        ''
        'function togglePomodoroTimer() {'
        '  var btn = document.getElementById("pomo-toggle-btn");'
        '  var status = document.getElementById("pomo-status-label");'
        '  var cel = document.getElementById("pomo-celebrate-box");'
        '  if (cel) cel.style.display = "none";'
        '  if (isRunning) {'
        '    clearInterval(timerInterval);'
        '    isRunning = false;'
        '    if (btn) btn.textContent = "▶️ Resume Focus";'
        '    if (status) status.textContent = "Paused";'
        '    stopAmbientSound();'
        '  } else {'
        '    isRunning = true;'
        '    if (btn) btn.textContent = "⏸️ Pause";'
        '    if (status) status.textContent = "Focus Active";'
        '    var sel = document.getElementById("pomo-audio-select");'
        '    if (sel && sel.value !== "none") switchAmbientSound(sel.value);'
        '    timerInterval = setInterval(function() {'
        '      if (leftSec > 0) {'
        '        leftSec--;'
        '        updateDisplay();'
        '      } else {'
        '        clearInterval(timerInterval);'
        '        isRunning = false;'
        '        if (btn) btn.textContent = "▶️ Start Next Block";'
        '        if (status) status.textContent = "Completed!";'
        '        if (cel) cel.style.display = "block";'
        '        playChime();'
        '        stopAmbientSound();'
        '      }'
        '    }, 1000);'
        '  }'
        '};'
        ''
        'function resetPomodoroTimer() {'
        '  clearInterval(timerInterval);'
        '  isRunning = false;'
        '  leftSec = totalSec;'
        '  updateDisplay();'
        '  var btn = document.getElementById("pomo-toggle-btn");'
        '  var status = document.getElementById("pomo-status-label");'
        '  var cel = document.getElementById("pomo-celebrate-box");'
        '  if (cel) cel.style.display = "none";'
        '  if (btn) btn.textContent = "▶️ Start Focus Block";'
        '  if (status) status.textContent = "Ready";'
        '  stopAmbientSound();'
        '};'
        ''
        'function updateDisplay() {'
        '  var m = Math.floor(leftSec / 60);'
        '  var s = leftSec % 60;'
        '  var disp = document.getElementById("pomo-timer-display");'
        '  if (disp) disp.textContent = (m < 10 ? "0" : "") + m + ":" + (s < 10 ? "0" : "") + s;'
        '  var circle = document.getElementById("pomo-progress-circle");'
        '  if (circle) {'
        '    var circum = 389.56;'
        '    var frac = totalSec > 0 ? (totalSec - leftSec) / totalSec : 0;'
        '    circle.style.strokeDashoffset = circum * (1 - frac);'
        '  }'
        '}'
        ''
        'function playChime() {'
        '  try {'
        '    var ctx = new (window.AudioContext || window.webkitAudioContext)();'
        '    var osc = ctx.createOscillator();'
        '    var g = ctx.createGain();'
        '    osc.type = "sine";'
        '    osc.frequency.setValueAtTime(587.33, ctx.currentTime);'
        '    osc.frequency.exponentialRampToValueAtTime(880, ctx.currentTime + 0.3);'
        '    g.gain.setValueAtTime(0.25, ctx.currentTime);'
        '    g.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 1.2);'
        '    osc.connect(g);'
        '    g.connect(ctx.destination);'
        '    osc.start();'
        '    osc.stop(ctx.currentTime + 1.2);'
        '  } catch(e) {}'
        '}'
        ''
        'function switchAmbientSound(type) {'
        '  stopAmbientSound();'
        '  if (type === "none" || !isRunning) return;'
        '  try {'
        '    audioCtx = new (window.AudioContext || window.webkitAudioContext)();'
        '    var bufferSize = 2 * audioCtx.sampleRate;'
        '    var noiseBuffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);'
        '    var output = noiseBuffer.getChannelData(0);'
        '    for (var i = 0; i < bufferSize; i++) {'
        '      output[i] = Math.random() * 2 - 1;'
        '    }'
        '    noiseNode = audioCtx.createBufferSource();'
        '    noiseNode.buffer = noiseBuffer;'
        '    noiseNode.loop = true;'
        '    var filter = audioCtx.createBiquadFilter();'
        '    if (type === "rain") { filter.type = "lowpass"; filter.frequency.value = 800; }'
        '    else if (type === "cafe") { filter.type = "bandpass"; filter.frequency.value = 450; filter.Q.value = 1.0; }'
        '    else { filter.type = "lowpass"; filter.frequency.value = 350; }'
        '    gainNode = audioCtx.createGain();'
        '    gainNode.gain.value = 0.05;'
        '    noiseNode.connect(filter);'
        '    filter.connect(gainNode);'
        '    gainNode.connect(audioCtx.destination);'
        '    noiseNode.start();'
        '  } catch(e) {}'
        '};'
        ''
        'function stopAmbientSound() {'
        '  if (noiseNode) { try { noiseNode.stop(); } catch(e){} noiseNode = null; }'
        '  if (audioCtx) { try { audioCtx.close(); } catch(e){} audioCtx = null; }'
        '}'
        '</script>'
    )

def render_hero():
    """Backward compatibility helper."""
    return ""

