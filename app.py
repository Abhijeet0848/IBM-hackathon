"""
AI Study Buddy & Personalized Learning Agent
Streamlit Main Application - Complete Multi-Tab Working Edition
"""

import os
import re
import time
import importlib
import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv

load_dotenv(override=True)

import src.styling
importlib.reload(src.styling)
import src.resource_finder
importlib.reload(src.resource_finder)
from src.styling import CUSTOM_CSS, render_top_nav, render_motivation_banner, render_quiz_results_dashboard, render_pomodoro_timer
from src.ingestion import DocumentIngestionPipeline
from src.llm_client import LLMClient
from src.rag_engine import RAGEngine
from src.quiz_evaluator import QuizEvaluator
from src.gamification import GamificationEngine
from src.study_planner import StudyPlanner
from src.resource_finder import ResourceFinder
from src.flashcard_engine import FlashcardEngine
from src.knowledge_radar import KnowledgeRadarEngine

# Page configuration
st.set_page_config(
    page_title="AI Study Buddy | Personalized Learning Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Persistent Chat Storage Helpers
CHAT_HISTORY_FILE = "./chroma_db/chat_history.json"

def load_stored_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        try:
            with open(CHAT_HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []

def save_stored_chat_history(history):
    try:
        os.makedirs("./chroma_db", exist_ok=True)
        with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

# Initialize Session States
if "ingestion_pipeline" not in st.session_state or not hasattr(st.session_state.ingestion_pipeline, "get_all_chunks"):
    st.session_state.ingestion_pipeline = DocumentIngestionPipeline(persist_directory="./chroma_db")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = load_stored_chat_history()

if "student_xp" not in st.session_state:
    st.session_state.student_xp = 0

if "study_streak" not in st.session_state:
    st.session_state.study_streak = 1

if "personalized_plan" not in st.session_state:
    st.session_state.personalized_plan = None

if "current_quiz" not in st.session_state:
    st.session_state.current_quiz = None

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

if "quiz_eval_results" not in st.session_state:
    st.session_state.quiz_eval_results = None

if "user_quiz_answers" not in st.session_state:
    st.session_state.user_quiz_answers = {}

if "current_flashcards" not in st.session_state:
    st.session_state.current_flashcards = None

if "page" in st.query_params:
    st.session_state.view_mode = st.query_params["page"]
elif "view_mode" not in st.session_state:
    st.session_state.view_mode = "homepage"

# Core Engine Initializations
gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY", "")
try:
    if not gemini_key and hasattr(st, "secrets"):
        gemini_key = st.secrets.get("GEMINI_API_KEY", "") or st.secrets.get("GOOGLE_API_KEY", "")
except Exception:
    pass

if "custom_gemini_key" in st.session_state and st.session_state.custom_gemini_key:
    gemini_key = st.session_state.custom_gemini_key.strip()

llm_client = LLMClient(
    provider="🌟 Google Gemini (Free Generous Tier)",
    api_key=gemini_key if gemini_key else None,
    model_id="gemini-1.5-flash"
)
rag_engine = RAGEngine(st.session_state.ingestion_pipeline, llm_client)
study_planner = StudyPlanner(llm_client)
stats = st.session_state.ingestion_pipeline.get_stats()

# ======================================================================
# VIEW 1: SEPARATE HOMEPAGE (SHOWN FIRST TO USERS)
# ======================================================================
def render_homepage(study_planner):
    # Hero Section
    st.markdown("""
    <div class="hero-container">
        <div class="hero-pill-badge">✨ IBM Bob Study Companion & Multi-LLM RAG</div>
        <div class="hero-h1">Master Any Syllabus <span class="hero-h1-gradient">3x Faster</span> with AI</div>
        <div class="hero-subtext">
            Transform course notes, lecture slides, and dense syllabi into personalized day-by-day study schedules,
            interactive Kahoot-style active recall quizzes, multi-persona AI tutoring, and verified academic references.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Primary "Start IBM Bob Study" Action Card
    with st.container(border=True):
        st.markdown("#### 🚀 Ready to Begin Your Learning Journey?")
        st.write("Launch your personalized AI study companion to generate custom day-by-day roadmaps from your uploaded course notes, solve doubts with multi-persona explainers, and test your knowledge with active recall drills.")
        st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
        col_btn1, col_btn2 = st.columns([2.5, 1.5])
        with col_btn1:
            if st.button("🚀 Launch AI Study Workspace", key="home_start_btn", type="primary", use_container_width=True):
                st.query_params["page"] = "workspace"
                st.session_state.view_mode = "workspace"
                st.rerun()
        with col_btn2:
            if st.button("📂 Explore Vector Store", key="home_vector_btn", use_container_width=True):
                st.query_params["page"] = "workspace"
                st.session_state.view_mode = "workspace"
                st.rerun()

    # 4 Core Pillars (Feature Grid)
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.markdown("### ⚡ AI Study Buddy Capabilities")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon-wrapper" style="background: #eff6ff; color: #2563eb;">📅</div>
            <div class="feature-title">Adaptive Syllabus Sequencer</div>
            <div class="feature-desc">
                Constructs balanced day-by-day learning roadmaps based on your target exam date and daily bandwidth, 
                incorporating 1-day and 3-day spaced repetition retention loops and 1-click <code>.ics</code> calendar exports.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon-wrapper" style="background: #f0fdf4; color: #16a34a;">💬</div>
            <div class="feature-title">Multi-Persona Cognitive Tutor</div>
            <div class="feature-desc">
                Switch seamlessly between <strong>Strict Syllabus Mode</strong> (grounded strictly in notes), 
                <strong>ELI10 Mode</strong> (intuitive analogies for beginners), and <strong>Enriched Deep Dives</strong> (historical origins + industry applications).
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_f2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon-wrapper" style="background: #faf5ff; color: #9333ea;">🎮</div>
            <div class="feature-title">Gamified Kahoot Quiz Arena</div>
            <div class="feature-desc">
                Generates dynamic multiple-choice drills with real-time active recall testing. 
                Earn XP, level up badges, build daily streaks, and review instant answer explanations.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon-wrapper" style="background: #fffbeb; color: #d97706;">🔍</div>
            <div class="feature-title">Semantic Vector Explorer</div>
            <div class="feature-desc">
                Inspect ChromaDB vector embeddings, search indexed chunk similarity distances, 
                and verify syllabus coverage with complete transparency.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 3-Step "How It Works"
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    st.markdown("### 🚀 How It Works in 3 Simple Steps")
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.markdown("""
        <div class="step-card">
            <div class="step-num">1</div>
            <div style="font-weight: 700; color: #0f172a; margin-bottom: 4px;">Upload Syllabus / Notes</div>
            <div style="font-size: 0.83rem; color: #64748b;">Drop your course PDF, markdown, or text notes in the planner. The system chunks and vectors your material instantly.</div>
        </div>
        """, unsafe_allow_html=True)

    with col_s2:
        st.markdown("""
        <div class="step-card">
            <div class="step-num">2</div>
            <div style="font-weight: 700; color: #0f172a; margin-bottom: 4px;">Generate Study Schedule</div>
            <div style="font-size: 0.83rem; color: #64748b;">Choose your days to exam, daily hours, and study strategy (Balanced, Exam Sprint, Deep Dive, or Spaced Repetition).</div>
        </div>
        """, unsafe_allow_html=True)

    with col_s3:
        st.markdown("""
        <div class="step-card">
            <div class="step-num">3</div>
            <div style="font-weight: 700; color: #0f172a; margin-bottom: 4px;">Learn, Drill & Master</div>
            <div style="font-size: 0.83rem; color: #64748b;">Track daily milestones, ask doubts with the AI Tutor, click verified academic references, and crush Kahoot quizzes.</div>
        </div>
        """, unsafe_allow_html=True)

    # Frequently Asked Questions Accordion
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    st.markdown("### 💡 Frequently Asked Questions")
    with st.expander("🛡️ How does the AI Tutor prevent hallucinations?"):
        st.write("In **Strict Syllabus Mode**, the multi-LLM RAG engine restricts its responses exclusively to the retrieved context chunks from your uploaded document. If a concept is not present in your notes, it explicitly states so and asks for clarification rather than making up answers.")

    with st.expander("📅 Can I sync the generated study schedule with my calendar?"):
        st.write("Yes! You can export your personalized day-by-day plan as an RFC 5545 `.ics` file with one click. This file can be imported directly into **Google Calendar, Apple Calendar, or Microsoft Outlook** with automatic reminders set for each study session.")

    with st.expander("🎮 How does the Kahoot Quiz Arena work?"):
        st.write("The quiz arena dynamically generates multiple-choice questions evaluated strictly against your uploaded syllabus. You can select any question count (from 3 to 100), receive instant scorecards, earn XP and streak points, and review in-depth explanations for every answer.")

# ======================================================================
# VIEW 2: STUDY WORKSPACE
# ======================================================================
def render_study_workspace(study_planner, rag_engine, llm_client, stats):
    # Dynamic non-repeating motivation tailored to uploaded course
    active_topic = ""
    if st.session_state.personalized_plan:
        active_topic = st.session_state.personalized_plan.get("modules_structure", {}).get("course_title", "")
    elif stats["total_chunks"] > 0:
        active_topic = "Course Syllabus"

    all_mantras = GamificationEngine.get_all_mindset_mantras(course_topic=active_topic)

    # Unified Top Sleek Navigation Bar with Level XP & Streak
    lvl_info = GamificationEngine.get_level_info(st.session_state.student_xp)
    st.markdown(render_top_nav(lvl_info, st.session_state.student_xp, st.session_state.study_streak, show_back=True), unsafe_allow_html=True)
    st.markdown(render_motivation_banner(all_mantras), unsafe_allow_html=True)

    # Main Navigation Tabs (Spacious & Immediately Accessible)
    tab_dashboard, tab_chat, tab_quiz, tab_flashcards, tab_explorer = st.tabs([
        "📅 Study Schedule Planner",
        "💬 Doubt Solver & Deep Dives",
        "🎮 Gamified Kahoot Quizzes",
        "🗂️ Interactive Flashcards",
        "🔍 Knowledge & Vector Explorer"
    ])

    # TAB 1: SYLLABUS INGESTION & PERSONALIZED STUDY PLAN
    with tab_dashboard:
        st.markdown("### 🗓️ Study Schedule Planner")
        st.caption("Generate an optimized, day-by-day learning roadmap customized to your exam date and study bandwidth.")

        if not st.session_state.personalized_plan:
            with st.container(border=True):
                st.markdown("##### 📁 1. Course Material & Syllabus Source")
                st.caption("Upload your syllabus document (PDF / TXT / MD) or type/paste your course syllabus directly:")
                
                stats = st.session_state.ingestion_pipeline.get_stats()
                col_src_l, col_src_r = st.columns([2.3, 1.3])
                
                planner_uploaded_file = None
                planner_pasted_text = ""

                with col_src_l:
                    input_mode = st.radio(
                        "Syllabus Input Method:",
                        ["📁 Upload PDF / TXT Document", "✍️ Paste Syllabus Text"],
                        horizontal=True,
                        key="planner_input_method"
                    )
                    
                    if input_mode == "📁 Upload PDF / TXT Document":
                        planner_uploaded_file = st.file_uploader(
                            "Select Syllabus File (PDF, TXT, MD):",
                            type=["pdf", "txt", "md"],
                            key="planner_file_uploader"
                        )
                    else:
                        planner_pasted_text = st.text_area(
                            "Paste Course Syllabus / Modules:",
                            placeholder="",
                            height=160,
                            key="planner_text_area"
                        )
                        if st.button("📥 Index Pasted Syllabus Text", key="btn_save_pasted_text", use_container_width=True):
                            if planner_pasted_text.strip():
                                with st.spinner("Indexing fresh syllabus text into vector store..."):
                                    import io
                                    st.session_state.ingestion_pipeline.reset_database()
                                    text_file = io.BytesIO(planner_pasted_text.strip().encode('utf-8'))
                                    text_file.name = "Pasted_Syllabus.txt"
                                    try:
                                        res = st.session_state.ingestion_pipeline.process_and_store(
                                            text_file,
                                            "Pasted_Syllabus.txt"
                                        )
                                        st.session_state.chat_history = []
                                        st.session_state.current_quiz = None
                                        st.success(f"✓ Successfully indexed {res['chunk_count']} chunks from new syllabus!")
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"Error indexing text: {str(e)}")
                            else:
                                st.warning("Please paste your syllabus text into the box above before indexing.")

                with col_src_r:
                    st.markdown('<div class="sidebar-section-title" style="margin-top: 0; font-size: 0.82rem; font-weight: 700; color: #475569; letter-spacing: 0.05em; margin-bottom: 8px;">📊 KNOWLEDGE INDEX</div>', unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="sidebar-stats-row" style="margin-bottom: 8px;">
                        <div class="sidebar-stat-box">
                            <div class="sidebar-stat-number">{stats['document_count']}</div>
                            <div class="sidebar-stat-label">DOCUMENTS</div>
                        </div>
                        <div class="sidebar-stat-box">
                            <div class="sidebar-stat-number">{stats['total_chunks']}</div>
                            <div class="sidebar-stat-label">CHUNKS</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if stats["unique_documents"]:
                        doc_names = ", ".join(stats["unique_documents"][:2])
                        st.caption(f"**Indexed:** {doc_names}")
                    else:
                        st.caption("*No documents indexed yet.*")
                    
                    if st.button("🗑️ Reset Knowledge Store", key="planner_reset_db_btn", use_container_width=True):
                        st.session_state.ingestion_pipeline.reset_database()
                        st.session_state.chat_history = []
                        st.session_state.current_quiz = None
                        st.session_state.personalized_plan = None
                        st.session_state.quiz_submitted = False
                        st.success("Database reset!")
                        st.rerun()

                st.markdown("---")
                st.markdown("##### ⚙️ 2. Plan Parameters")
                st.caption("Define your target timeline, daily availability, and learning strategy.")
                
                col_p1, col_p2, col_p3 = st.columns(3)
                with col_p1:
                    input_days = st.number_input("Days Until Target / Exam:", min_value=1, max_value=60, value=7, step=1, key="sched_days_input")
                with col_p2:
                    input_hours = st.slider("Daily Study Hours:", min_value=0.5, max_value=8.0, value=2.0, step=0.5, key="sched_hours_input")
                with col_p3:
                    strategy_options = [
                        ("Balanced (Theory & Practice)", "balanced"),
                        ("Exam Sprint (High-Yield Drills)", "exam_sprint"),
                        ("Deep Dive (Theory & Derivations)", "deep_dive"),
                        ("Spaced Repetition (Retention)", "spaced_repetition")
                    ]
                    selected_strategy = st.selectbox(
                        "Learning Strategy:",
                        strategy_options,
                        format_func=lambda x: x[0],
                        index=0,
                        key="sched_strategy_select"
                    )[1]

                with st.expander("Advanced Configuration"):
                    col_o1, col_o2 = st.columns(2)
                    with col_o1:
                        level_options = [("Beginner", "beginner"), ("Intermediate", "intermediate"), ("Advanced", "advanced")]
                        selected_level = st.selectbox("Current Knowledge Level:", level_options, format_func=lambda x: x[0], index=1, key="sched_level_select")[1]
                    with col_o2:
                        include_rest = st.checkbox("Include Periodic Review Days", value=False, key="sched_rest_days_cb")

                st.markdown("<br>", unsafe_allow_html=True)
                generate_plan_btn = st.button("Generate Study Plan", type="primary", use_container_width=True, key="btn_gen_ai_schedule")

            if generate_plan_btn:
                context_text = ""
                # 1. Process Pasted Text if active
                if input_mode == "✍️ Paste Syllabus Text" and planner_pasted_text.strip():
                    with st.spinner("Indexing fresh syllabus text..."):
                        import io
                        st.session_state.ingestion_pipeline.reset_database()
                        text_file = io.BytesIO(planner_pasted_text.strip().encode('utf-8'))
                        text_file.name = "Pasted_Syllabus.txt"
                        try:
                            res = st.session_state.ingestion_pipeline.process_and_store(
                                text_file,
                                "Pasted_Syllabus.txt"
                            )
                            context_text = planner_pasted_text.strip()
                            st.toast(f"✓ Indexed {res['chunk_count']} new syllabus chunks")
                        except Exception as e:
                            st.error(f"Text indexing error: {str(e)}")

                # 2. Process Uploaded File if active
                elif input_mode == "📁 Upload PDF / TXT Document" and planner_uploaded_file is not None:
                    with st.spinner("Processing & indexing uploaded syllabus file..."):
                        st.session_state.ingestion_pipeline.reset_database()
                        try:
                            res = st.session_state.ingestion_pipeline.process_and_store(
                                planner_uploaded_file,
                                planner_uploaded_file.name
                            )
                            all_chunks = st.session_state.ingestion_pipeline.get_all_chunks(limit=40)
                            context_text = "\n\n".join([c["content"] for c in all_chunks])
                            st.toast(f"✓ Ingested '{res['filename']}' ({res['chunk_count']} chunks)")
                        except Exception as e:
                            st.error(f"File ingestion error: {str(e)}")

                # 3. Fallback to existing vector store
                if not context_text:
                    all_chunks = st.session_state.ingestion_pipeline.get_all_chunks(limit=40)
                    if all_chunks:
                        context_text = "\n\n".join([c["content"] for c in all_chunks])
                    elif planner_pasted_text.strip():
                        context_text = planner_pasted_text.strip()

                if not context_text.strip():
                    st.warning("⚠️ Please upload a syllabus file (PDF/TXT) or paste your course topics above first!")
                else:
                    with st.spinner("Analyzing syllabus and sequencing daily milestones..."):
                        plan_res = study_planner.generate_personalized_plan(
                            context_text=context_text,
                            days=int(input_days),
                            hours_per_day=float(input_hours),
                            study_strategy=selected_strategy,
                            student_level=selected_level if 'selected_level' in locals() else "intermediate",
                            include_rest_days=include_rest if 'include_rest' in locals() else False
                        )
                        st.session_state.personalized_plan = plan_res
                        reward = GamificationEngine.award_xp(st.session_state.student_xp, "complete_milestone")
                        st.session_state.student_xp = reward["new_xp"]
                        st.toast(f"🎉 +{reward['earned_xp']} XP for generating your roadmap!")
                        st.rerun()

        else:
            # Display Active Personalized Plan (Clean & Sleek)
            plan = st.session_state.personalized_plan
            sched = plan.get("schedule", {})
            days_list = sched.get("days", [])
            analytics = study_planner.get_plan_analytics(plan)

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

            # Quick Actions Toolbar
            st.markdown("<br>", unsafe_allow_html=True)
            t_col1, t_col2, t_col3, t_col4 = st.columns([1.5, 1.5, 1.5, 1])
            with t_col1:
                ics_content = study_planner.export_to_ics(plan)
                st.download_button("📅 Export to Calendar (.ics)", data=ics_content, file_name="study_plan.ics", mime="text/calendar", use_container_width=True)
            with t_col2:
                md_content = study_planner.export_to_markdown(plan)
                st.download_button("📄 Export Markdown (.md)", data=md_content, file_name="study_roadmap.md", mime="text/markdown", use_container_width=True)
            with t_col3:
                with st.popover("⚙️ Adjust Schedule"):
                    st.markdown("**Adaptive Rebalancer**")
                    st.caption("Recalculate remaining incomplete days.")
                    reb_days = st.number_input("Revised Target Days:", min_value=1, max_value=30, value=max(1, analytics['total_days'] - analytics['completed_days']))
                    reb_hrs = st.slider("Revised Daily Hours:", min_value=0.5, max_value=8.0, value=float(sched.get('hours_per_day', 2.0)), step=0.5)
                    if st.button("Apply Rebalance", type="primary", use_container_width=True):
                        st.session_state.personalized_plan = study_planner.rebalance_schedule(plan, new_target_days=int(reb_days), new_hours_per_day=float(reb_hrs))
                        st.toast("✨ Schedule rebalanced!")
                        st.rerun()
            with t_col4:
                if st.button("New Plan", use_container_width=True):
                    st.session_state.personalized_plan = None
                    st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)

            # Interactive Pomodoro Focus Timer
            components.html(render_pomodoro_timer(), height=310)

            # Filter Options
            filt_c1, filt_c2 = st.columns([3, 1])
            with filt_c1:
                filter_mode = st.radio("Filter Sessions:", ["All Sessions", "Pending Only", "Completed"], horizontal=True, label_visibility="collapsed", key="sched_filter_mode")
            with filt_c2:
                st.markdown(f"<div style='text-align: right; color: #94a3b8; font-size: 0.85rem; padding-top: 6px;'>{len(days_list)} Days Planned</div>", unsafe_allow_html=True)

            # Day-by-Day Clean Streamlit Containers
            for d in days_list:
                d_num = d.get("day_number")
                is_done = d.get("completed", False)
                focus_mod = d.get("focus_module", f"Day {d_num}")
                mins = d.get("estimated_time_minutes", 120)
                checkpoint = d.get("checkpoint", "Milestone Target")

                if filter_mode == "Pending Only" and is_done:
                    continue
                if filter_mode == "Completed" and not is_done:
                    continue

                with st.container(border=True):
                    h_col1, h_col2 = st.columns([3.5, 1.5])
                    with h_col1:
                        status_icon = "✓" if is_done else "●"
                        status_color = "#10b981" if is_done else "#2563eb"
                        st.markdown(f"""
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="color: {status_color}; font-weight: bold; font-size: 1.1rem;">{status_icon}</span>
                            <span style="font-weight: 700; font-size: 1.05rem; color: #0f172a;">Day {d_num}: {focus_mod}</span>
                            <span style="background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; padding: 0.15rem 0.5rem; border-radius: 6px; font-size: 0.75rem; font-weight: 600;">~{mins} mins</span>
                        </div>
                        """, unsafe_allow_html=True)
                    with h_col2:
                        st.markdown(f"""
                        <div style="text-align: right;">
                            <span style="background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; padding: 0.2rem 0.55rem; border-radius: 6px; font-size: 0.75rem; font-weight: 600;">🎯 {checkpoint}</span>
                        </div>
                        """, unsafe_allow_html=True)

                    spaced = d.get("spaced_review_topic")
                    if spaced and spaced != "None" and "None" not in spaced:
                        st.markdown(f"""
                        <div style="background: #f5f3ff; border: 1px solid #ddd6fe; border-left: 3px solid #6366f1; padding: 0.4rem 0.75rem; border-radius: 8px; font-size: 0.82rem; color: #4338ca; margin-top: 0.5rem; margin-bottom: 0.6rem;">
                            <strong>🧠 Spaced Review (10-15m):</strong> {spaced}
                        </div>
                        """, unsafe_allow_html=True)

                    col_tasks, col_actions = st.columns([3.5, 1.2])
                    with col_tasks:
                        if "completed_tasks" not in d:
                            d["completed_tasks"] = []
                        
                        tasks_arr = d.get("tasks", [])
                        for t_idx, t in enumerate(tasks_arr):
                            is_t_done = t_idx in d["completed_tasks"] or is_done
                            t_checked = st.checkbox(
                                t,
                                value=is_t_done,
                                key=f"chk_task_{d_num}_{t_idx}"
                            )
                            if t_checked != (t_idx in d["completed_tasks"]):
                                if t_checked:
                                    if t_idx not in d["completed_tasks"]:
                                        d["completed_tasks"].append(t_idx)
                                        reward = GamificationEngine.award_xp(st.session_state.student_xp, "ask_question")
                                        st.session_state.student_xp = reward["new_xp"]
                                        st.toast(f"✅ Subtopic completed! +{reward['earned_xp']} XP")
                                else:
                                    if t_idx in d["completed_tasks"]:
                                        d["completed_tasks"].remove(t_idx)
                                
                                # If all tasks in day checked, mark day complete
                                if len(d["completed_tasks"]) == len(tasks_arr) and len(tasks_arr) > 0:
                                    d["completed"] = True
                                elif not t_checked and d.get("completed"):
                                    d["completed"] = False
                                st.rerun()

                    with col_actions:
                        with st.popover("📚 References", use_container_width=True):
                            tasks_list = d.get("tasks", [])
                            res_data = ResourceFinder.get_curated_resources_for_day(focus_mod, checkpoint, tasks_list)
                            
                            # Dynamic Topic & Domain Header
                            domain_badge = res_data.get("domain", "Academic Studies")
                            popover_html = (
                                f'<div class="popover-header" style="flex-direction: column; align-items: flex-start; gap: 4px;">'
                                f'<div><span>🎯</span> <strong>Focus:</strong> {res_data["primary_topic"]}</div>'
                                f'<div style="font-size: 0.74rem; font-weight: 700; color: #6366f1; background: #eef2ff; padding: 2px 8px; border-radius: 12px; border: 1px solid #c7d2fe;">🏷️ {domain_badge}</div>'
                                f'</div>'
                                f'<div class="resource-tile-list">'
                            )
                            for tile in res_data.get("resource_tiles", []):
                                popover_html += f'<a href="{tile["url"]}" target="_blank" class="resource-tile {tile.get("color", "resource-tile-blue")}"><span>{tile["title"]}</span><span>↗</span></a>'
                            popover_html += '</div>'
                            st.markdown(popover_html, unsafe_allow_html=True)
                            
                            # Subtopics
                            if res_data.get("subtopics"):
                                sub_html = '<div class="subtopics-label">📑 Subtopic Deep Dives</div><div class="resource-tile-list">'
                                for sub in res_data["subtopics"]:
                                    sub_html += f'<a href="{sub["wikipedia_url"]}" target="_blank" class="resource-tile resource-tile-blue" style="font-size: 0.78rem; padding: 0.45rem 0.75rem;"><span>📘 {sub["name"]}</span><span>↗</span></a>'
                                sub_html += '</div>'
                                st.markdown(sub_html, unsafe_allow_html=True)

                        if not is_done:
                            if st.button("Complete All", key=f"btn_chk_{d_num}", type="primary", use_container_width=True):
                                d["completed"] = True
                                d["completed_tasks"] = list(range(len(d.get("tasks", []))))
                                reward = GamificationEngine.award_xp(st.session_state.student_xp, "complete_milestone")
                                st.session_state.student_xp = reward["new_xp"]
                                st.rerun()
                        else:
                            if st.button("Reset Day", key=f"btn_unchk_{d_num}", use_container_width=True):
                                d["completed"] = False
                                d["completed_tasks"] = []
                                st.rerun()

    # ----------------------------------------------------------------------
    # TAB 2: KNOWLEDGE RETRIEVAL & ENRICHED CONTENT
    # ----------------------------------------------------------------------
    with tab_chat:
        col_chat_h, col_chat_clr = st.columns([3.8, 1.4])
        with col_chat_h:
            st.markdown("### 💬 Interactive AI Study Tutor & Enriched Deep Dives")
            st.caption("Ask questions about your uploaded syllabus or select specialized cognitive delivery personas.")
        with col_chat_clr:
            if st.session_state.chat_history:
                md_notes = "# AI Study Buddy — Study Q&A Notes\n\n"
                for m in st.session_state.chat_history:
                    if m["role"] == "user":
                        md_notes += f"### 🧑‍🎓 Question: {m['content']}\n\n"
                    else:
                        md_notes += f"#### 🤖 Answer ({m.get('mode', 'tutor').title()} Mode):\n{m['content']}\n\n---\n\n"
                c_btn1, c_btn2 = st.columns(2)
                with c_btn1:
                    st.download_button("💾 Save", data=md_notes, file_name="study_chat_notes.md", mime="text/markdown", use_container_width=True)
                with c_btn2:
                    if st.button("🗑️ Clear", key="btn_clear_chat", use_container_width=True):
                        st.session_state.chat_history = []
                        save_stored_chat_history([])
                        st.rerun()

        col_m, col_i = st.columns([1.8, 3.2])
        with col_m:
            chat_mode = st.radio(
                "Select AI Delivery Persona:",
                [
                    ("🎓 Strict Syllabus Tutor", "strict"),
                    ("🎈 ELI10 (Child-Friendly)", "eli10"),
                    ("💡 Enriched Delivery (Core + History + Future)", "enriched")
                ],
                format_func=lambda x: x[0],
                index=0
            )
            selected_mode_key = chat_mode[1]

        with col_i:
            if selected_mode_key == "strict":
                st.info("🔒 **Strict Tutor:** Answers ONLY with syllabus facts. Refuses out-of-scope questions with *'This is not in your syllabus'*.")
            elif selected_mode_key == "eli10":
                st.info("🎈 **ELI10 Mode:** Explains dense technical concepts using intuitive real-world analogies (Lego blocks, playground see-saws).")
            else:
                st.info("💡 **Enriched Delivery:** Comprehensive 3-part breakdown: **Core Mechanics**, **Historical Origin Story**, and **Modern Industry/Future Research**.")

        if stats["total_chunks"] == 0:
            st.warning("⚠️ No documents uploaded yet. Upload your PDF or notes in the Study Schedule Planner to enable RAG answers.")

        # Prominent Inline Question Bar (Cleanly placed in tab, not pinned to bottom)
        with st.form("chat_inline_form", clear_on_submit=True):
            col_inp, col_btn = st.columns([4.8, 1.2])
            with col_inp:
                prompt_text = st.text_input(
                    "Ask Tutor:",
                    placeholder="Type your syllabus question and press Enter...",
                    label_visibility="collapsed",
                    key="inline_tutor_prompt"
                )
            with col_btn:
                ask_submit = st.form_submit_button("🚀 Ask Tutor", type="primary", use_container_width=True)

        user_prompt = prompt_text.strip() if (ask_submit and prompt_text.strip()) else None

        if user_prompt:
            st.session_state.chat_history.append({"role": "user", "content": user_prompt})
            with st.spinner("Analyzing syllabus and querying AI Tutor..."):
                response_obj = rag_engine.answer_query(
                    query=user_prompt,
                    mode=selected_mode_key
                )
                answer_text = response_obj["answer"]
                citations = response_obj["context_chunks"]

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer_text,
                    "mode": selected_mode_key,
                    "citations": citations
                })
                save_stored_chat_history(st.session_state.chat_history)

                reward = GamificationEngine.award_xp(
                    st.session_state.student_xp,
                    "view_enriched_content" if selected_mode_key == "enriched" else "ask_question"
                )
                st.session_state.student_xp = reward["new_xp"]
                st.toast(f"✨ +{reward['earned_xp']} XP earned!")
                st.rerun()

        # Render Chat History (Direct Click-to-Edit on User Questions)
        for idx, msg in enumerate(st.session_state.chat_history):
            if msg["role"] == "user":
                with st.chat_message("user", avatar="🧑‍🎓"):
                    user_q_val = st.text_input(
                        "Question",
                        value=msg["content"],
                        key=f"user_inline_q_{idx}",
                        label_visibility="collapsed",
                        help="Click text to edit your question, then press Enter to regenerate"
                    )
                    # If the student edited the question and pressed Enter
                    if user_q_val and user_q_val.strip() != msg["content"]:
                        st.session_state.chat_history = st.session_state.chat_history[:idx]
                        st.session_state.chat_history.append({"role": "user", "content": user_q_val.strip()})
                        
                        with st.spinner("Regenerating answer with updated question..."):
                            response_obj = rag_engine.answer_query(
                                query=user_q_val.strip(),
                                mode=selected_mode_key
                            )
                            st.session_state.chat_history.append({
                                "role": "assistant",
                                "content": response_obj["answer"],
                                "mode": selected_mode_key,
                                "citations": response_obj["context_chunks"]
                            })
                            save_stored_chat_history(st.session_state.chat_history)
                        st.rerun()
            else:
                with st.chat_message("assistant", avatar="💡" if msg.get("mode") == "enriched" else ("🎓" if msg.get("mode") == "strict" else "🧒")):
                    st.markdown(msg["content"])
                    if "citations" in msg and msg["citations"]:
                        # Filter out fragments and clean leading severed characters
                        valid_citations = []
                        seen_c_texts = set()
                        for c in msg["citations"]:
                            raw_c = c.get("content", "").strip()
                            clean_c = re.sub(r'^(?:[a-zA-Z]\s+|tion\s+|ing\s+|ers\s+|eristics\b[\s\.\,]*)', '', raw_c, flags=re.IGNORECASE).strip()
                            if clean_c and len(clean_c) >= 20 and clean_c.lower() not in seen_c_texts:
                                clean_c = clean_c[0].upper() + clean_c[1:]
                                seen_c_texts.add(clean_c.lower())
                                valid_citations.append((c.get("metadata", {}).get("source", "Syllabus"), clean_c))

                        if valid_citations:
                            with st.expander(f"🔍 View {len(valid_citations)} Verified Syllabus Citations"):
                                for c_idx, (src, c_text) in enumerate(valid_citations):
                                    st.markdown(f"**Chunk #{c_idx+1} (`{src}`):**")
                                    st.code(c_text, language="markdown")

    # ----------------------------------------------------------------------
    # TAB 3: GAMIFIED KAHOOT-STYLE QUIZZES
    # ----------------------------------------------------------------------
    with tab_quiz:
        st.markdown("### 🎮 Gamified Kahoot-Style AI Quiz Arena")
        st.caption("Active recall drills with live scoring, XP multipliers, and detailed explanations.")

        if stats["total_chunks"] == 0:
            st.info("👈 Upload your syllabus in the Study Schedule Planner first to generate custom AI quizzes.")

        q_col1, q_col2, q_col3 = st.columns([2.5, 1.2, 1.3])
        with q_col1:
            quiz_topic = st.text_input(
                "🎯 Focus Topic / Concept (Optional):",
                placeholder="Leave blank to get quiz of entire syllabus or topics",
                key="quiz_topic_field"
            )
        with q_col2:
            num_questions = st.number_input(
                "🔢 Question Count:",
                min_value=3,
                max_value=100,
                value=8,
                step=1,
                key="quiz_num_questions"
            )
        with q_col3:
            st.write("")
            st.write("")
            btn_label = "🔄 Regenerate Quiz" if st.session_state.current_quiz else "🔥 Launch AI Quiz"
            gen_quiz_btn = st.button(btn_label, type="primary", use_container_width=True)

        if gen_quiz_btn:
            if stats["total_chunks"] == 0:
                st.warning("Please upload course materials in the Study Schedule Planner first!")
            else:
                with st.spinner(f"Extracting {num_questions} high-yield syllabus questions from your uploaded document..."):
                    query = f"Generate {num_questions} multiple choice questions on {quiz_topic}" if quiz_topic else f"Generate {num_questions} comprehensive multiple choice questions covering the syllabus"
                    quiz_resp = rag_engine.answer_query(query=query, mode="quiz", top_k=25, question_count=int(num_questions))

                    if quiz_resp["quiz_data"]:
                        quiz_obj = quiz_resp["quiz_data"]
                        quiz_obj["title"] = f"AI Quiz on: {quiz_topic.title() if quiz_topic else 'Full Course Syllabus'} ({len(quiz_obj.get('questions', []))} Questions)"
                        st.session_state.quiz_instance_id = int(time.time() * 1000)
                        st.session_state.current_quiz = quiz_obj
                        st.session_state.quiz_submitted = False
                        st.session_state.quiz_eval_results = None
                        st.session_state.user_quiz_answers = {}
                        st.success(f"Generated {len(quiz_obj.get('questions', []))} questions! Select your answers below:")
                        st.rerun()
                    else:
                        st.error("Could not parse quiz output. Please try clicking Launch AI Quiz again.")

        # Render Kahoot-Style Quiz Form
        if st.session_state.current_quiz:
            quiz = st.session_state.current_quiz
            st.markdown(f"#### 🏆 {quiz.get('title', 'Syllabus Quiz')}")
            st.markdown("---")

            questions = quiz.get("questions", [])
            q_inst_id = st.session_state.get("quiz_instance_id", 0)

            with st.form(key=f"kahoot_quiz_form_{q_inst_id}"):
                for q in questions:
                    qid = q.get("id")
                    q_text = q.get("question")
                    options = q.get("options", {})
                    
                    st.markdown(
                        f'<div class="kahoot-card">'
                        f'<div class="kahoot-q-badge">🎯 Question {qid} of {len(questions)} • ⚡ +25 XP</div>'
                        f'<div class="kahoot-question-title">{q_text}</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                    
                    radio_options = [f"[{opt_key}] {opt_val}" for opt_key, opt_val in options.items()]
                    
                    current_choice = st.radio(
                        f"Answer for Q{qid}:",
                        radio_options,
                        key=f"kahoot_q_{q_inst_id}_{qid}",
                        label_visibility="collapsed"
                    )
                    
                    if current_choice:
                        if "[" in current_choice and "]" in current_choice:
                            selected_key = current_choice.split("[")[1].split("]")[0].strip()
                        else:
                            selected_key = current_choice.split(":")[0].strip()
                        st.session_state.user_quiz_answers[qid] = selected_key

                submit_kahoot = st.form_submit_button("🏁 Submit Quiz & Claim XP", type="primary", use_container_width=True)

            if submit_kahoot:
                st.session_state.quiz_submitted = True
                eval_res = QuizEvaluator.evaluate_quiz(
                    quiz,
                    st.session_state.user_quiz_answers
                )
                st.session_state.quiz_eval_results = eval_res
                
                bonus_xp = (eval_res["correct_count"] * 25) + 50
                st.session_state.student_xp += bonus_xp
                st.toast(f"🎉 Quiz Complete! +{bonus_xp} XP Added to your profile!")
                st.rerun()

            # Results breakdown
            if st.session_state.quiz_submitted and st.session_state.quiz_eval_results:
                res = st.session_state.quiz_eval_results
                tot_q = res.get("total_questions", len(res.get("breakdown", [])))
                corr_q = res.get("correct_count", 0)
                wrong_q = res.get("wrong_count", max(0, tot_q - corr_q))
                score_p = res.get("score_pct", round(corr_q / tot_q * 100, 1) if tot_q > 0 else 0)
                badge = res.get("badge", "Mastery")
                badge_class = res.get("badge_class", "badge-green")
                feedback = res.get("feedback", "Great work on completing the quiz drill!")

                st.markdown("---")
                st.markdown(render_quiz_results_dashboard(res), unsafe_allow_html=True)

                # Visual Knowledge Radar & Weak-Area Diagnostics
                diag = KnowledgeRadarEngine.analyze_quiz_diagnostics(res)
                if diag["topics"]:
                    st.markdown(KnowledgeRadarEngine.render_diagnostic_dashboard_html(diag), unsafe_allow_html=True)

                    if diag["needs_remediation"] and diag["weakest_topic"]:
                        weak_topic = diag["weakest_topic"]
                        col_rem1, col_rem2 = st.columns([3.2, 1.8])
                        with col_rem1:
                            st.info(f"💡 **AI Adaptive Remediation:** Launch a targeted 1-Day Sprint on **{weak_topic}** to transform this weak area into mastery.")
                        with col_rem2:
                            st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
                            if st.button(f"⚡ Generate 1-Day Sprint Plan", key="btn_gen_remediation_plan", type="primary", use_container_width=True):
                                all_chunks = st.session_state.ingestion_pipeline.get_all_chunks(limit=30)
                                ctx = f"Focused Remediation Sprint on: {weak_topic}\n" + "\n".join([c["content"] for c in all_chunks[:6]])
                                st.session_state.personalized_plan = study_planner.generate_study_schedule(
                                    context_text=ctx,
                                    days=1,
                                    hours_per_day=2.0,
                                    strategy_key="exam_cram",
                                    level_key="intermediate"
                                )
                                st.toast(f"✨ 1-Day Remediation Plan for '{weak_topic}' Created! Open Tab 1 to start.")
                                st.rerun()

                with st.expander("📋 View Detailed Question Review & Correct Answers", expanded=False):
                    for item in res.get("breakdown", []):
                        if item["is_correct"]:
                            st.success(
                                f"**✅ Question {item['id']}: {item['question']}**\n\n"
                                f"• **Your Answer:** `[{item['user_answer']}] {item['user_answer_text']}` *(Correct!)*\n\n"
                                f"💡 **Explanation & Concept Rule:** {item['explanation']}"
                            )
                        else:
                            st.error(
                                f"**❌ Question {item['id']}: {item['question']}**\n\n"
                                f"• **Your Choice (Incorrect):** `[{item['user_answer']}] {item['user_answer_text']}`\n\n"
                                f"• **✅ Correct Answer:** `[{item['correct_answer']}] {item['correct_answer_text']}`\n\n"
                                f"💡 **Why this is correct:** {item['explanation']}"
                            )

    # ----------------------------------------------------------------------
    # TAB 4: INTERACTIVE AI FLASHCARDS
    # ----------------------------------------------------------------------
    with tab_flashcards:
        st.markdown("### 🗂️ Interactive AI Flashcard & Spaced Recall Arena")
        st.caption("Auto-extract key definitions, core formulas, and fundamental principles into interactive 3D flip cards with Leitner spaced repetition sorting.")

        if stats["total_chunks"] == 0:
            st.warning("⚠️ No documents uploaded yet. Upload a syllabus in the Study Schedule Planner to generate custom flashcards.")
        else:
            fc_col1, fc_col2, fc_col3 = st.columns([1.5, 1.5, 2.5])
            with fc_col1:
                card_count = st.selectbox("Deck Size:", [4, 8, 12, 16, 20], index=1, key="fc_deck_size_select")
            with fc_col2:
                st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                if st.button("✨ Generate Deck", type="primary", use_container_width=True, key="btn_gen_flashcards"):
                    all_chunks = st.session_state.ingestion_pipeline.get_all_chunks(limit=30)
                    ctx = "\n\n".join([c["content"] for c in all_chunks])
                    with st.spinner("Synthesizing active recall flashcards from syllabus..."):
                        cards = FlashcardEngine.generate_flashcards(ctx, count=int(card_count), llm_client=llm_client)
                        st.session_state.current_flashcards = cards
                        reward = GamificationEngine.award_xp(st.session_state.student_xp, "ask_question")
                        st.session_state.student_xp = reward["new_xp"]
                        st.toast(f"🎉 Generated {len(cards)} flashcards! +{reward['earned_xp']} XP")
                        st.rerun()
            with fc_col3:
                if st.session_state.current_flashcards:
                    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                    fc_md = "# AI Study Buddy — Flashcard Deck\n\n"
                    for fc in st.session_state.current_flashcards:
                        fc_md += f"### ❓ Q: {fc['front']}\n**💡 Answer:** {fc['back']}\n*Category: {fc.get('category', 'General')}*\n\n---\n\n"
                    st.download_button("💾 Export Deck (.md)", data=fc_md, file_name="study_flashcards.md", mime="text/markdown", use_container_width=True)

            # Auto-generate starter cards if none yet
            if not st.session_state.current_flashcards:
                all_chunks = st.session_state.ingestion_pipeline.get_all_chunks(limit=30)
                if all_chunks:
                    ctx = "\n\n".join([c["content"] for c in all_chunks])
                    st.session_state.current_flashcards = FlashcardEngine.generate_flashcards(ctx, count=8, llm_client=None)

            if st.session_state.current_flashcards:
                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                components.html(FlashcardEngine.render_interactive_flashcard_deck(st.session_state.current_flashcards), height=440)

    # ----------------------------------------------------------------------
    # TAB 5: VECTOR DB & KNOWLEDGE EXPLORER
    # ----------------------------------------------------------------------
    with tab_explorer:
        st.markdown("### 🔍 ChromaDB Vector Knowledge Explorer")
        st.caption("Inspect and debug the local vector store index, search distances, and all extracted document chunks.")

        all_stored_chunks = st.session_state.ingestion_pipeline.get_all_chunks(limit=50)

        t4_col1, t4_col2 = st.columns([2.5, 1.5])
        with t4_col1:
            search_query = st.text_input("Test Vector Similarity Query:", placeholder="Type a concept keyword to test vector cosine search...")
        with t4_col2:
            st.write("")
            st.write("")
            test_search_btn = st.button("🔎 Run Vector Search", use_container_width=True)

        if search_query:
            test_chunks = st.session_state.ingestion_pipeline.query_similarity(search_query, n_results=5)
            if test_chunks:
                st.markdown(f"##### 🎯 Found **{len(test_chunks)}** Vector Matches:")
                for idx, ch in enumerate(test_chunks):
                    with st.expander(f"Match #{idx+1} | Source: `{ch['metadata'].get('source')}` | Distance: {round(ch.get('distance', 0.0), 3)}"):
                        st.markdown(f"**Content:**\n\n{ch['content']}")
                        st.json(ch['metadata'])
            else:
                st.warning("No matching vector chunks found.")
        
        st.markdown("---")
        col_hdr_l, col_hdr_r = st.columns([3.5, 1.5])
        with col_hdr_l:
            st.markdown(f"### 📂 All Ingested Document Chunks ({len(all_stored_chunks)} total)")
        with col_hdr_r:
            if st.button("🗑️ Clear Vector Database", key="tab4_clear_db_btn", use_container_width=True):
                st.session_state.ingestion_pipeline.reset_database()
                st.session_state.chat_history = []
                st.session_state.current_quiz = None
                st.success("Vector database cleared! Please re-index your syllabus.")
                st.rerun()
        
        if all_stored_chunks:
            for idx, ch in enumerate(all_stored_chunks):
                src = ch["metadata"].get("source", "Uploaded File")
                ch_idx = ch["metadata"].get("chunk_index", idx)
                char_len = ch["metadata"].get("char_length", len(ch["content"]))
                
                with st.expander(f"Chunk #{idx+1} — File: `{src}` (Index: {ch_idx}, Length: {char_len} chars)"):
                    st.code(ch["content"], language="markdown")
                    st.caption(f"Chunk ID: `{ch['id']}`")
        else:
            st.info("No chunks indexed yet. Upload a PDF or text file in the Study Schedule Planner to populate the ChromaDB knowledge base.")

# ======================================================================
# MAIN EXECUTION ROUTER
# ======================================================================
if st.session_state.view_mode == "homepage":
    render_homepage(study_planner)
else:
    render_study_workspace(study_planner, rag_engine, llm_client, stats)

