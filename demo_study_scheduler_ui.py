"""
Professional, Sleek, and Clean Study Scheduler UI
Enterprise/SaaS Grade Design - Minimalist & Polished
"""

import datetime
import streamlit as st
from src.llm_client import LLMClient
from src.study_planner import StudyPlanner
from src.resource_finder import ResourceFinder

# Set page configuration
st.set_page_config(
    page_title="AI Study Scheduler",
    page_icon="🗓️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional SaaS Theme CSS (Light)
PROFESSIONAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global resets & typography */
html, body, [class*="css"], .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    background-color: #f8fafc !important;
    color: #0f172a !important;
}

/* App Header */
.app-header {
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 1.25rem;
    margin-bottom: 1.75rem;
}
.app-title {
    font-size: 1.75rem;
    font-weight: 700;
    color: #0f172a;
    letter-spacing: -0.02em;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.app-desc {
    font-size: 0.95rem;
    color: #475569;
    margin-top: 0.35rem;
    line-height: 1.5;
}

/* Card Containers */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
    transition: border-color 0.15s ease;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: #93c5fd !important;
}

/* Inputs & Selectboxes */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div,
.stTextArea > div > div > textarea {
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
    color: #0f172a !important;
    font-size: 0.9rem !important;
}
.stTextInput > div > div > input:focus,
.stSelectbox > div > div:focus-within {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 1px #2563eb !important;
}

/* Buttons */
.stButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.15s ease !important;
}
.stButton > button[kind="primary"] {
    background: #2563eb !important;
    color: #ffffff !important;
    border: none !important;
}
.stButton > button[kind="primary"]:hover {
    background: #1d4ed8 !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25) !important;
}
.stButton > button:not([kind="primary"]) {
    background: #f1f5f9 !important;
    color: #1e293b !important;
    border: 1px solid #cbd5e1 !important;
}
.stButton > button:not([kind="primary"]):hover {
    background: #e2e8f0 !important;
    color: #0f172a !important;
}

/* Clean Progress Bar */
.stProgress > div > div > div > div {
    background-color: #2563eb !important;
}

/* Metric Display */
[data-testid="stMetricValue"] {
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    color: #0f172a !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.8rem !important;
    color: #64748b !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
}

/* Tags & Badges */
.tag {
    display: inline-block;
    padding: 0.2rem 0.55rem;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.02em;
}
.tag-indigo { background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }
.tag-emerald { background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; }
.tag-slate { background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; }

/* Task List Style */
.task-bullet {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-left: 3px solid #2563eb;
    border-radius: 6px;
    padding: 0.5rem 0.75rem;
    margin-bottom: 0.4rem;
    font-size: 0.88rem;
    color: #1e293b;
    line-height: 1.4;
}
</style>
"""
st.markdown(PROFESSIONAL_CSS, unsafe_allow_html=True)

# State initialization
if "plan" not in st.session_state:
    st.session_state.plan = None
if "xp" not in st.session_state:
    st.session_state.xp = 100

SAMPLE_SYLLABI = {
    "Artificial Intelligence & Machine Learning": """Course: Artificial Intelligence & Machine Learning
Module 1: Foundations of Supervised Learning (Linear Regression, Loss Functions, Gradient Descent)
Module 2: Regularization & Model Validation (Overfitting, L1/L2 Regularization, Cross Validation, ROC Curves)
Module 3: Decision Trees & Ensemble Methods (Random Forests, Gradient Boosting, XGBoost)
Module 4: Deep Neural Networks (Backpropagation, Activation Functions, CNNs, Transformers)
Module 5: Unsupervised Clustering & Embeddings (K-Means, PCA, Vector Embeddings)""",
    "Data Structures & Algorithms": """Course: Data Structures & Algorithms
Module 1: Graph Theory & Shortest Paths (BFS, DFS, Dijkstra, Bellman-Ford)
Module 2: Dynamic Programming Techniques (0/1 Knapsack, Longest Common Subsequence, Matrix Chain)
Module 3: Advanced Tree Architectures (AVL Trees, Red-Black Trees, Segment Trees, Tries)
Module 4: Computational Complexity (P vs NP, Approximation Algorithms, Vertex Cover)""",
    "Cloud Architecture & Distributed Systems": """Course: Cloud Architecture & Distributed Systems
Module 1: Networking & API Protocols (HTTP/2, WebSockets, gRPC, REST Design)
Module 2: Microservices & Scalability (API Gateways, JWT Security, Service Mesh)
Module 3: Distributed Storage (CAP Theorem, ACID vs BASE, NoSQL Systems, Sharding)
Module 4: Caching & Edge Infrastructure (Redis Architecture, CDN Distribution, Load Balancing)"""
}

# Sidebar - Clean & Purposeful
with st.sidebar:
    st.markdown("#### 📚 Syllabus Source")
    syllabus_choice = st.selectbox(
        "Select Course Material:",
        list(SAMPLE_SYLLABI.keys()) + ["Custom Input..."],
        index=0
    )
    
    if syllabus_choice == "Custom Input...":
        syllabus_text = st.text_area("Paste Course Outline / Topics:", height=180, placeholder="Module 1: ...\nModule 2: ...")
    else:
        syllabus_text = SAMPLE_SYLLABI[syllabus_choice]
        with st.expander("View Selected Syllabus"):
            st.text(syllabus_text)

    st.divider()
    st.caption(f"🏆 **Gamified Progress:** `{st.session_state.xp} XP`")
    if st.session_state.plan:
        if st.button("Reset Study Plan", use_container_width=True):
            st.session_state.plan = None
            st.rerun()

# Instantiate planner
llm = LLMClient()
planner = StudyPlanner(llm)

# Clean Professional Header
st.markdown("""
<div class="app-header">
    <div class="app-title">
        <span>🗓️ Study Schedule Planner</span>
    </div>
    <div class="app-desc">
        Generate an optimized, day-by-day learning roadmap customized to your exam date and study bandwidth.
    </div>
</div>
""", unsafe_allow_html=True)

# Main UI Flow
if not st.session_state.plan:
    # Schedule Configuration Card
    with st.container(border=True):
        st.markdown("##### ⚙️ Plan Parameters")
        st.caption("Define your target timeline, daily availability, and learning strategy.")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            days = st.number_input("Days Until Target / Exam:", min_value=1, max_value=60, value=7, step=1)
        with c2:
            hours = st.slider("Daily Study Hours:", min_value=0.5, max_value=8.0, value=2.0, step=0.5)
        with c3:
            strategy = st.selectbox(
                "Learning Strategy:",
                [
                    ("Balanced (Theory & Practice)", "balanced"),
                    ("Exam Sprint (High-Yield Drills)", "exam_sprint"),
                    ("Deep Dive (Theory & Derivations)", "deep_dive"),
                    ("Spaced Repetition (Memory Retention)", "spaced_repetition")
                ],
                format_func=lambda x: x[0]
            )[1]

        with st.expander("Advanced Configuration"):
            adv_c1, adv_c2 = st.columns(2)
            with adv_c1:
                level = st.selectbox("Current Knowledge Level:", [("Beginner", "beginner"), ("Intermediate", "intermediate"), ("Advanced", "advanced")], index=1, format_func=lambda x: x[0])[1]
            with adv_c2:
                include_buffer = st.checkbox("Include Periodic Review Days", value=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Generate Study Plan", type="primary", use_container_width=True):
            if not syllabus_text.strip():
                st.warning("Please select or paste syllabus text in the sidebar.")
            else:
                with st.spinner("Analyzing syllabus and sequencing daily milestones..."):
                    plan = planner.generate_personalized_plan(
                        context_text=syllabus_text,
                        days=int(days),
                        hours_per_day=float(hours),
                        study_strategy=strategy,
                        student_level=level,
                        include_rest_days=include_buffer
                    )
                    st.session_state.plan = plan
                    st.session_state.xp += 50
                    st.rerun()

else:
    # Active Plan View
    plan = st.session_state.plan
    sched = plan.get("schedule", {})
    days_list = sched.get("days", [])
    analytics = planner.get_plan_analytics(plan)

    # 1. Summary Metrics & Progress Bar
    with st.container(border=True):
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Progress", f"{analytics['completion_pct']}%", f"{analytics['completed_days']}/{analytics['total_days']} Days")
        with m2:
            st.metric("Hours Logged", f"{analytics['completed_hours']}h", f"of {analytics['total_hours']}h total")
        with m3:
            st.metric("Action Items", f"{analytics['total_tasks']}", "Checklist tasks")
        with m4:
            strat_name = sched.get("study_strategy", "balanced").replace("_", " ").title()
            st.metric("Strategy", strat_name, "Active Mode")

        st.progress(analytics["completion_pct"] / 100.0)

    # 2. Action Toolbar (Clean Row)
    act_c1, act_c2, act_c3, act_c4 = st.columns([1.5, 1.5, 1.5, 1])
    with act_c1:
        ics_data = planner.export_to_ics(plan)
        st.download_button(
            "📅 Export to Calendar (.ics)",
            data=ics_data,
            file_name="study_plan.ics",
            mime="text/calendar",
            use_container_width=True
        )
    with act_c2:
        md_data = planner.export_to_markdown(plan)
        st.download_button(
            "📄 Export Markdown Guide (.md)",
            data=md_data,
            file_name="study_guide.md",
            mime="text/markdown",
            use_container_width=True
        )
    with act_c3:
        with st.popover("⚙️ Adjust Schedule"):
            st.markdown("**Adaptive Rebalancer**")
            st.caption("Recalculate remaining incomplete days.")
            new_days = st.number_input("Revised Target Days:", min_value=1, max_value=30, value=max(1, analytics['total_days'] - analytics['completed_days']))
            new_hrs = st.slider("Revised Daily Hours:", min_value=0.5, max_value=8.0, value=float(sched.get("hours_per_day", 2.0)), step=0.5)
            if st.button("Apply Rebalance", type="primary", use_container_width=True):
                st.session_state.plan = planner.rebalance_schedule(plan, new_target_days=int(new_days), new_hours_per_day=float(new_hrs))
                st.rerun()
    with act_c4:
        if st.button("New Plan", use_container_width=True):
            st.session_state.plan = None
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Filter Bar
    f1, f2 = st.columns([3, 1])
    with f1:
        filter_mode = st.radio(
            "Filter Sessions:",
            ["All Sessions", "Pending Only", "Completed"],
            horizontal=True,
            label_visibility="collapsed"
        )
    with f2:
        st.markdown(f"<div style='text-align: right; color: #94a3b8; font-size: 0.85rem; padding-top: 6px;'>{len(days_list)} Days Planned</div>", unsafe_allow_html=True)

    # 4. Day by Day Timeline Cards (Sleek Streamlit Containers)
    for d in days_list:
        d_num = d.get("day_number")
        is_done = d.get("completed", False)
        focus = d.get("focus_module", f"Day {d_num}")
        mins = d.get("estimated_time_minutes", 120)
        checkpoint = d.get("checkpoint", "Milestone Target")

        if filter_mode == "Pending Only" and is_done:
            continue
        if filter_mode == "Completed" and not is_done:
            continue

        with st.container(border=True):
            # Card Header
            h_col1, h_col2 = st.columns([3.5, 1.5])
            with h_col1:
                status_icon = "✓" if is_done else "●"
                status_color = "#34d399" if is_done else "#818cf8"
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="color: {status_color}; font-weight: bold; font-size: 1.1rem;">{status_icon}</span>
                    <span style="font-weight: 700; font-size: 1.05rem; color: #ffffff;">Day {d_num}: {focus}</span>
                    <span class="tag tag-slate">~{mins} mins</span>
                </div>
                """, unsafe_allow_html=True)
            with h_col2:
                st.markdown(f"""
                <div style="text-align: right;">
                    <span class="tag tag-emerald">🎯 {checkpoint}</span>
                </div>
                """, unsafe_allow_html=True)

            # Spaced repetition alert if exists
            spaced = d.get("spaced_review_topic")
            if spaced and spaced != "None" and "None" not in spaced:
                st.markdown(f"""
                <div style="background: rgba(99, 102, 241, 0.08); border-left: 3px solid #6366f1; padding: 0.35rem 0.65rem; border-radius: 4px; font-size: 0.82rem; color: #c7d2fe; margin-top: 0.5rem; margin-bottom: 0.5rem;">
                    <strong>Spaced Review (10-15m):</strong> {spaced}
                </div>
                """, unsafe_allow_html=True)

            # Task List & Action in neat 2 columns
            t_col, b_col = st.columns([3.5, 1.2])
            with t_col:
                for t in d.get("tasks", []):
                    st.markdown(f"<div class='task-bullet'>{t}</div>", unsafe_allow_html=True)

            with b_col:
                # Reference links popover
                with st.popover("📚 References", use_container_width=True):
                    first_task = d.get("tasks", [focus])[0]
                    res = ResourceFinder.get_curated_resources(first_task)
                    st.markdown(f"**Topic:** *{res['topic'][:35]}*")
                    st.markdown(f"- [▶️ **YouTube Video Lectures**]({res['youtube_url']})")
                    st.markdown(f"- [📖 **Textbooks & Literature**]({res['google_books_url']})")
                    st.markdown(f"- [🎓 **MIT OpenCourseWare**]({res['mit_ocw_url']})")
                    st.markdown(f"- [🌐 **Wikipedia Concept**]({res['wikipedia_url']})")

                # Mark Done / Undo Button
                if not is_done:
                    if st.button("Mark Completed", key=f"d_done_{d_num}", type="primary", use_container_width=True):
                        d["completed"] = True
                        st.session_state.xp += 50
                        st.rerun()
                else:
                    if st.button("Mark Incomplete", key=f"d_undo_{d_num}", use_container_width=True):
                        d["completed"] = False
                        st.rerun()
