"""
Comprehensive Premium Design System for AI Study Buddy
Engineered for modern dark-mode glassmorphism, vibrant gradients, and smooth micro-interactions.
"""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

/* Base application styling */
.stApp {
    background: radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(236, 72, 153, 0.06) 0%, transparent 40%),
                #090d16 !important;
    color: #f1f5f9 !important;
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.75) !important;
    backdrop-filter: blur(20px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
}

section[data-testid="stSidebar"] .stMarkdown h3 {
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.01em !important;
    color: #cbd5e1 !important;
    margin-top: 0.5rem !important;
}

/* Hero Header Component */
.hero-header {
    background: linear-gradient(135deg, rgba(30, 27, 75, 0.8) 0%, rgba(15, 23, 42, 0.95) 50%, rgba(49, 46, 129, 0.6) 100%);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 20px;
    padding: 2rem 2.25rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    position: relative;
    overflow: hidden;
}

.hero-header::after {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(99, 102, 241, 0.2) 0%, transparent 70%);
    pointer-events: none;
}

.hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin: 0;
    background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #f472b6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.hero-subtitle {
    color: #94a3b8;
    font-size: 1rem;
    line-height: 1.6;
    margin-top: 0.6rem;
    max-width: 850px;
}

/* Badges */
.badge {
    display: inline-flex;
    align-items: center;
    padding: 0.3rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    text-transform: uppercase;
}

.badge-blue { background: rgba(59, 130, 246, 0.18); color: #93c5fd; border: 1px solid rgba(59, 130, 246, 0.4); }
.badge-purple { background: rgba(168, 85, 247, 0.18); color: #d8b4fe; border: 1px solid rgba(168, 85, 247, 0.4); }
.badge-green { background: rgba(34, 197, 94, 0.18); color: #86efac; border: 1px solid rgba(34, 197, 94, 0.4); }
.badge-amber { background: rgba(245, 158, 11, 0.18); color: #fcd34d; border: 1px solid rgba(245, 158, 11, 0.4); }
.badge-rose { background: rgba(244, 63, 94, 0.18); color: #fda4af; border: 1px solid rgba(244, 63, 94, 0.4); }

/* Gamified Quote Banner */
.quote-card {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.85) 100%);
    border-left: 4px solid #f59e0b;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    border-right: 1px solid rgba(255, 255, 255, 0.08);
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 1rem 1.25rem;
    color: #e2e8f0;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
}

.quote-text {
    font-size: 0.95rem;
    font-style: italic;
    color: #f8fafc;
    line-height: 1.5;
}

.quote-author {
    font-size: 0.8rem;
    color: #fbbf24;
    font-weight: 700;
    margin-top: 0.4rem;
    text-align: right;
}

/* XP Level Tracker Card */
.xp-banner {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
    border: 1px solid rgba(99, 102, 241, 0.35);
    border-radius: 14px;
    padding: 1rem 1.25rem;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
}

.xp-title {
    font-weight: 800;
    color: #f8fafc;
    font-size: 1.05rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.4rem;
}

/* Modern Tab Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(15, 23, 42, 0.6);
    padding: 6px;
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    margin-bottom: 1.5rem;
}

.stTabs [data-baseweb="tab"] {
    height: 44px;
    border-radius: 10px;
    color: #94a3b8 !important;
    font-weight: 600;
    font-size: 0.9rem;
    padding: 0 1.25rem;
    border: none !important;
    transition: all 0.2s ease;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%) !important;
    color: #ffffff !important;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4) !important;
}

/* Streamlit Buttons Transformation */
.stButton > button {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 10px !important;
    padding: 0.55rem 1.25rem !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25) !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(37, 99, 235, 0.45) !important;
    border-color: rgba(255, 255, 255, 0.3) !important;
}

/* Primary Action Buttons */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.35) !important;
}

.stButton > button[kind="primary"]:hover {
    box-shadow: 0 8px 25px rgba(99, 102, 241, 0.55) !important;
}

/* Inputs & Form Controls */
.stTextInput > div > div > input, .stSelectbox > div > div, .stNumberInput > div > div > input {
    background: rgba(15, 23, 42, 0.7) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 10px !important;
    color: #f8fafc !important;
    font-size: 0.92rem !important;
}

.stTextInput > div > div > input:focus, .stSelectbox > div > div:focus-within {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25) !important;
}

/* Chat Messages */
div[data-testid="stChatMessage"] {
    background: rgba(15, 23, 42, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 16px !important;
    padding: 1.25rem !important;
    margin-bottom: 1rem !important;
    backdrop-filter: blur(10px) !important;
}

div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.7) 100%) !important;
    border-left: 3px solid #38bdf8 !important;
}

div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) {
    background: linear-gradient(135deg, rgba(49, 46, 129, 0.25) 0%, rgba(15, 23, 42, 0.7) 100%) !important;
    border-left: 3px solid #a855f7 !important;
}

/* Kahoot Quiz Question Card */
.kahoot-card {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
}

.kahoot-question-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.75rem;
    line-height: 1.4;
}

/* Roadmap Milestone Card */
.milestone-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 1.15rem;
    margin-bottom: 0.75rem;
    transition: all 0.2s ease;
}

.milestone-card:hover {
    border-color: rgba(99, 102, 241, 0.4);
    background: rgba(255, 255, 255, 0.05);
}

/* Metrics Pill */
.metric-pill {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 0.65rem 0.85rem;
    border-radius: 12px;
    text-align: center;
}

.metric-val {
    font-size: 1.35rem;
    font-weight: 800;
    background: linear-gradient(135deg, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.metric-label {
    font-size: 0.7rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-weight: 600;
}

/* Expanders */
.streamlit-expanderHeader {
    background: rgba(15, 23, 42, 0.5) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    color: #cbd5e1 !important;
}
</style>
"""

def render_hero():
    """Renders the top hero header banner."""
    return """
    <div class="hero-header">
        <div class="hero-title">
            <span>🧠 AI Study Buddy</span>
            <span class="badge badge-purple">Multi-LLM RAG Engine</span>
            <span class="badge badge-green">Gamified XP</span>
        </div>
        <div class="hero-subtitle">
            Your personalized learning copilot. Index your course materials for 
            <strong>Strict Syllabus QA</strong>, <strong>ELI10 Real-World Analogies</strong>, 
            <strong>Enriched Deep Dives</strong>, and <strong>Kahoot-Style Gamified Quizzes</strong>.
        </div>
    </div>
    """
