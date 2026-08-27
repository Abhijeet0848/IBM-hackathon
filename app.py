"""
AI Study Buddy & Personalized Learning Agent
Streamlit Main Application - Complete Multi-Tab Working Edition
"""

import os
import time
import streamlit as st
from dotenv import load_dotenv

load_dotenv(override=True)

from src.styling import CUSTOM_CSS, render_hero
from src.ingestion import DocumentIngestionPipeline
from src.llm_client import LLMClient
from src.rag_engine import RAGEngine
from src.quiz_evaluator import QuizEvaluator
from src.gamification import GamificationEngine
from src.study_planner import StudyPlanner
from src.resource_finder import ResourceFinder

# Page configuration
st.set_page_config(
    page_title="AI Study Buddy | Personalized Learning Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Initialize Session States
if "ingestion_pipeline" not in st.session_state or not hasattr(st.session_state.ingestion_pipeline, "get_all_chunks"):
    st.session_state.ingestion_pipeline = DocumentIngestionPipeline(persist_directory="./chroma_db")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

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

# Sidebar: Controls & Syllabus Ingestion
with st.sidebar:
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY", "")
    llm_client = LLMClient(
        provider="🌟 Google Gemini (Free Generous Tier)",
        api_key=gemini_key if gemini_key else None,
        model_id="gemini-flash-latest"
    )
    rag_engine = RAGEngine(st.session_state.ingestion_pipeline, llm_client)
    study_planner = StudyPlanner(llm_client)

    st.markdown("### 🧠 AI Study Buddy")
    st.markdown('<span class="badge badge-green">● Gemini AI Core Online</span>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📚 Syllabus Ingestion (RAG)")
    
    uploaded_files = st.file_uploader(
        "Upload Syllabus / Lecture Notes (PDF/TXT)",
        type=["pdf", "txt", "md"],
        accept_multiple_files=True
    )

    if uploaded_files:
        if st.button("🚀 Ingest into ChromaDB", use_container_width=True, type="primary"):
            with st.spinner("Parsing & embedding document chunks into vector database..."):
                for uploaded_file in uploaded_files:
                    try:
                        res = st.session_state.ingestion_pipeline.process_and_store(
                            uploaded_file,
                            uploaded_file.name
                        )
                        st.success(f"✓ Ingested '{res['filename']}' ({res['chunk_count']} chunks)")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                st.rerun()

    # Knowledge Stats
    stats = st.session_state.ingestion_pipeline.get_stats()
    st.markdown("---")
    st.markdown("### 📊 Knowledge Stats")
    st.markdown(f"""
    <div style="display: flex; gap: 8px; margin-bottom: 10px;">
        <div class="metric-pill" style="flex: 1;">
            <div class="metric-val">{stats['document_count']}</div>
            <div class="metric-label">Documents</div>
        </div>
        <div class="metric-pill" style="flex: 1;">
            <div class="metric-val">{stats['total_chunks']}</div>
            <div class="metric-label">Chunks</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if stats["unique_documents"]:
        st.caption("Active: " + ", ".join(stats["unique_documents"][:3]))

    if st.button("🗑️ Clear Vector Database", use_container_width=True):
        st.session_state.ingestion_pipeline.reset_database()
        st.session_state.chat_history = []
        st.session_state.current_quiz = None
        st.session_state.personalized_plan = None
        st.session_state.quiz_submitted = False
        st.success("Database cleared!")
        st.rerun()

# Top Hero Banner
st.markdown(render_hero(), unsafe_allow_html=True)

# Gamification Banner & Motivational Reminders
lvl_info = GamificationEngine.get_level_info(st.session_state.student_xp)
daily_quote = GamificationEngine.get_daily_smart_reminder()

col_g1, col_g2 = st.columns([1.6, 2.4])
with col_g1:
    st.markdown(f"""
    <div class="xp-banner">
        <div>
            <div class="xp-title">{lvl_info['icon']} Level {lvl_info['current_level']}: {lvl_info['title']}</div>
            <span class="badge badge-purple">{st.session_state.student_xp} Total XP</span>
            <span class="badge badge-amber">🔥 {st.session_state.study_streak} Day Streak</span>
        </div>
        <div style="text-align: right;">
            <span style="font-size: 0.78rem; color: #94a3b8;">Next Level: {lvl_info['next_level_xp']} XP</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(lvl_info['progress_pct'] / 100)

with col_g2:
    st.markdown(f"""
    <div class="quote-card">
        <div class="quote-text">🔔 <strong>Smart Reminder:</strong> "{daily_quote['quote']}"</div>
        <div class="quote-author">— {daily_quote['author']}</div>
    </div>
    """, unsafe_allow_html=True)

# Main Navigation Tabs
tab_dashboard, tab_chat, tab_quiz, tab_explorer = st.tabs([
    "📅 1. Personalization & Schedule (SLLM)",
    "💬 2. Knowledge Retrieval & Enriched Content",
    "🎮 3. Gamified Kahoot-Style Quizzes",
    "🔍 4. Vector DB & Knowledge Explorer"
])

# ----------------------------------------------------------------------
# TAB 1: SYLLABUS INGESTION & PERSONALIZED STUDY PLAN
# ----------------------------------------------------------------------
with tab_dashboard:
    st.markdown("### 🗓️ Study Schedule Planner")
    st.caption("Generate an optimized, day-by-day learning roadmap customized to your exam date and study bandwidth.")

    if stats["total_chunks"] == 0:
        st.info("👈 **Get Started:** Upload your syllabus or course notes in the left sidebar to generate a custom schedule.")

    if not st.session_state.personalized_plan:
        with st.container(border=True):
            st.markdown("##### ⚙️ Plan Parameters")
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
            if stats["total_chunks"] == 0:
                st.warning("Please upload a syllabus or notes in the sidebar first!")
            else:
                with st.spinner("Analyzing syllabus and sequencing daily milestones..."):
                    all_chunks = st.session_state.ingestion_pipeline.get_all_chunks(limit=40)
                    context_text = "\n\n".join([c["content"] for c in all_chunks])
                    
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
                    status_color = "#34d399" if is_done else "#818cf8"
                    st.markdown(f"""
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="color: {status_color}; font-weight: bold; font-size: 1.1rem;">{status_icon}</span>
                        <span style="font-weight: 700; font-size: 1.05rem; color: #ffffff;">Day {d_num}: {focus_mod}</span>
                        <span style="background: rgba(148, 163, 184, 0.15); color: #cbd5e1; padding: 0.15rem 0.5rem; border-radius: 6px; font-size: 0.75rem; font-weight: 600;">~{mins} mins</span>
                    </div>
                    """, unsafe_allow_html=True)
                with h_col2:
                    st.markdown(f"""
                    <div style="text-align: right;">
                        <span style="background: rgba(16, 185, 129, 0.15); color: #6ee7b7; border: 1px solid rgba(16, 185, 129, 0.3); padding: 0.2rem 0.55rem; border-radius: 6px; font-size: 0.75rem; font-weight: 600;">🎯 {checkpoint}</span>
                    </div>
                    """, unsafe_allow_html=True)

                spaced = d.get("spaced_review_topic")
                if spaced and spaced != "None" and "None" not in spaced:
                    st.markdown(f"""
                    <div style="background: rgba(99, 102, 241, 0.08); border-left: 3px solid #6366f1; padding: 0.35rem 0.65rem; border-radius: 4px; font-size: 0.82rem; color: #c7d2fe; margin-top: 0.5rem; margin-bottom: 0.5rem;">
                        <strong>Spaced Review (10-15m):</strong> {spaced}
                    </div>
                    """, unsafe_allow_html=True)

                col_tasks, col_actions = st.columns([3.5, 1.2])
                with col_tasks:
                    for t in d.get("tasks", []):
                        st.markdown(f"<div style='background: #0f172a; border: 1px solid rgba(255, 255, 255, 0.06); border-left: 3px solid #6366f1; border-radius: 6px; padding: 0.5rem 0.75rem; margin-bottom: 0.4rem; font-size: 0.88rem; color: #e2e8f0;'>{t}</div>", unsafe_allow_html=True)

                with col_actions:
                    with st.popover("📚 References", use_container_width=True):
                        first_task = d.get("tasks", [focus_mod])[0]
                        res_data = ResourceFinder.get_curated_resources(first_task)
                        st.markdown(f"**Topic:** *{res_data['topic'][:35]}*")
                        st.markdown(f"- [▶️ **YouTube Video Lectures**]({res_data['youtube_url']})")
                        st.markdown(f"- [📖 **Textbooks & Books**]({res_data['google_books_url']})")
                        st.markdown(f"- [🎓 **MIT OpenCourseWare**]({res_data['mit_ocw_url']})")
                        st.markdown(f"- [🌐 **Wikipedia Overview**]({res_data['wikipedia_url']})")

                    if not is_done:
                        if st.button("Mark Completed", key=f"btn_chk_{d_num}", type="primary", use_container_width=True):
                            d["completed"] = True
                            reward = GamificationEngine.award_xp(st.session_state.student_xp, "complete_milestone")
                            st.session_state.student_xp = reward["new_xp"]
                            st.rerun()
                    else:
                        if st.button("Mark Incomplete", key=f"btn_unchk_{d_num}", use_container_width=True):
                            d["completed"] = False
                            st.rerun()

# ----------------------------------------------------------------------
# TAB 2: KNOWLEDGE RETRIEVAL & ENRICHED CONTENT
# ----------------------------------------------------------------------
with tab_chat:
    st.markdown("### 💬 Interactive AI Study Tutor & Enriched Deep Dives")
    st.caption("Ask questions about your uploaded syllabus or select specialized cognitive delivery personas.")

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
        st.warning("⚠️ No documents uploaded yet. Upload your PDF or notes in the left sidebar to enable RAG answers.")

    # Render Chat History
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"], avatar="🧑‍🎓" if msg["role"] == "user" else ("💡" if msg.get("mode") == "enriched" else ("🎓" if msg.get("mode") == "strict" else "🧒"))):
            st.markdown(msg["content"])
            if "citations" in msg and msg["citations"]:
                with st.expander(f"🔍 View {len(msg['citations'])} Verified Syllabus Citations"):
                    for c_idx, c in enumerate(msg["citations"]):
                        src = c["metadata"].get("source", "Syllabus")
                        st.markdown(f"**Chunk #{c_idx+1} (`{src}`):**")
                        st.code(c["content"], language="markdown")

    # Chat Input Box
    user_prompt = st.chat_input("Ask a question about your uploaded syllabus...")

    if user_prompt:
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})
        with st.chat_message("user", avatar="🧑‍🎓"):
            st.markdown(user_prompt)

        with st.chat_message("assistant", avatar="💡" if selected_mode_key == "enriched" else ("🎓" if selected_mode_key == "strict" else "🧒")):
            with st.spinner("Searching ChromaDB vector store & querying Gemini..."):
                response_obj = rag_engine.answer_query(
                    query=user_prompt,
                    mode=selected_mode_key
                )
                answer_text = response_obj["answer"]
                citations = response_obj["context_chunks"]

                st.markdown(answer_text)

                if citations:
                    with st.expander(f"🔍 View {len(citations)} Verified Syllabus Citations"):
                        for c_idx, c in enumerate(citations):
                            src = c["metadata"].get("source", "Syllabus")
                            st.markdown(f"**Chunk #{c_idx+1} (`{src}`):**")
                            st.code(c["content"], language="markdown")

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer_text,
                    "mode": selected_mode_key,
                    "citations": citations
                })

                reward = GamificationEngine.award_xp(
                    st.session_state.student_xp,
                    "view_enriched_content" if selected_mode_key == "enriched" else "ask_question"
                )
                st.session_state.student_xp = reward["new_xp"]
                st.toast(f"✨ +{reward['earned_xp']} XP earned!")
                st.rerun()

# ----------------------------------------------------------------------
# TAB 3: GAMIFIED KAHOOT-STYLE QUIZZES
# ----------------------------------------------------------------------
with tab_quiz:
    st.markdown("### 🎮 Gamified Kahoot-Style AI Quiz Arena")
    st.caption("Active recall drills with live scoring, XP multipliers, and detailed explanations.")

    if stats["total_chunks"] == 0:
        st.info("👈 Upload your syllabus in the sidebar first to generate custom AI quizzes.")

    q_col1, q_col2, q_col3 = st.columns([2.6, 1.2, 1.2])
    with q_col1:
        quiz_topic = st.text_input(
            "🎯 Focus Topic / Concept (Optional):",
            placeholder="e.g. Pointers, Malloc, or leave blank for full syllabus",
            key="quiz_topic_field"
        )
    with q_col2:
        num_questions = st.number_input(
            "🔢 Question Count:",
            min_value=3,
            max_value=30,
            value=10,
            step=1,
            key="quiz_num_questions"
        )
    with q_col3:
        st.write("")
        st.write("")
        gen_quiz_btn = st.button("🔥 Launch AI Quiz", type="primary", use_container_width=True)

    if gen_quiz_btn:
        if stats["total_chunks"] == 0:
            st.warning("Please upload course materials in the sidebar first!")
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
        opt_icons = {"A": "🔴", "B": "🔷", "C": "🟡", "D": "🟢"}
        q_inst_id = st.session_state.get("quiz_instance_id", 0)

        with st.form(key=f"kahoot_quiz_form_{q_inst_id}"):
            for q in questions:
                qid = q.get("id")
                q_text = q.get("question")
                options = q.get("options", {})
                
                st.markdown(f"""
                <div class="kahoot-card">
                    <div class="kahoot-question-title">Question {qid}: {q_text}</div>
                </div>
                """, unsafe_allow_html=True)
                
                radio_options = [f"{opt_icons.get(opt_key, '⚪')} [{opt_key}] {opt_val}" for opt_key, opt_val in options.items()]
                
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
            st.markdown("---")
            st.markdown("### 🏅 Score Breakdown & Leaderboard Status")
            
            c_s1, c_s2, c_s3 = st.columns(3)
            with c_s1:
                st.metric("Total Score", f"{res['correct_count']} / {res['total_questions']}")
            with c_s2:
                st.metric("Accuracy", f"{res['score_pct']}%")
            with c_s3:
                st.markdown(f"**Rank Tier:** <span class='badge {res['badge_class']}'>{res['badge']}</span>", unsafe_allow_html=True)
                st.caption(res['feedback'])

            st.markdown("#### 📋 Question Review & Explanations:")
            for item in res["breakdown"]:
                if item["is_correct"]:
                    st.success(f"**Q{item['id']}: {item['question']}**\n\n✅ Your answer: `[{item['user_answer']}] {item['user_answer_text']}`\n\n💡 *Explanation:* {item['explanation']}")
                else:
                    st.error(f"**Q{item['id']}: {item['question']}**\n\n❌ Your answer: `[{item['user_answer']}] {item['user_answer_text']}`\n\n✅ Correct answer: `[{item['correct_answer']}] {item['correct_answer_text']}`\n\n💡 *Explanation:* {item['explanation']}")

# ----------------------------------------------------------------------
# TAB 4: VECTOR DB & KNOWLEDGE EXPLORER
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
    st.markdown(f"### 📂 All Ingested Document Chunks ({len(all_stored_chunks)} total)")
    
    if all_stored_chunks:
        for idx, ch in enumerate(all_stored_chunks):
            src = ch["metadata"].get("source", "Uploaded File")
            ch_idx = ch["metadata"].get("chunk_index", idx)
            char_len = ch["metadata"].get("char_length", len(ch["content"]))
            
            with st.expander(f"Chunk #{idx+1} — File: `{src}` (Index: {ch_idx}, Length: {char_len} chars)"):
                st.code(ch["content"], language="markdown")
                st.caption(f"Chunk ID: `{ch['id']}`")
    else:
        st.info("No chunks indexed yet. Upload a PDF or text file in the sidebar to populate the ChromaDB knowledge base.")
