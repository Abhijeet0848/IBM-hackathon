"""
Study Planner & Syllabus Analyzer
Performs deep topic extraction, prerequisite sequencing, and builds a realistic,
syllabus-specific day-by-day study schedule with spaced repetition, adaptive rebalancing,
and calendar export capabilities from the student's uploaded notes.
"""

import json
import re
import datetime
from typing import Dict, Any, List, Optional
from src.llm_client import LLMClient

COMPREHENSIVE_SCHEDULE_PROMPT = """You are an expert academic curriculum designer and study schedule planner.
Analyze the following uploaded student course notes/syllabus and construct a customized, day-by-day study roadmap.

CRITICAL INSTRUCTIONS:
1. You MUST extract the REAL topics, module titles, formulas, algorithms, definitions, and mechanisms from the provided text below.
2. DO NOT use generic placeholders like "Foundations & Core Principles", "Read introductory sections", "Complete notes summary".
3. Every day MUST focus on a specific topic from the context (e.g. "Linear Regression & Overfitting", "Linked Lists & Floyd's Cycle Detection", "Glycolysis & Krebs Cycle").
4. For each day, create 3-4 detailed, concrete action items structured into 3 distinct learning phases:
   - 📖 [Foundation/Theory]: Study exact definitions, theorems, or mechanisms from the notes.
   - 🛠️ [Practice/Application]: Solve problems, analyze code, or write out formulas.
   - 🧠 [Active Recall / Review]: Test recall using flashcards, ELI10 self-explanation, or quiz drills.
5. Create a specific Target Milestone for each day reflecting the actual concept mastered.
6. Target Study Strategy: {strategy_desc}
7. Target Student Level: {level_desc}
8. Distribute the material across exactly {days} days with a target load of {hours_per_day} hours/day.
9. Return strictly a valid JSON object matching the schema below.

REQUIRED JSON SCHEMA:
{{
  "course_title": "Specific Course Title from Uploaded Context",
  "study_strategy": "{strategy}",
  "student_level": "{level}",
  "modules": [
    {{
      "module_number": 1,
      "module_name": "Exact Module Title from Text",
      "difficulty": "Beginner | Intermediate | Advanced",
      "estimated_hours": 4,
      "topics": ["Specific Topic 1", "Specific Topic 2", "Specific Topic 3"]
    }}
  ],
  "schedule": {{
    "plan_title": "Personalized {days}-Day Study Plan ({hours_per_day} hrs/day)",
    "total_days": {days},
    "hours_per_day": {hours_per_day},
    "days": [
      {{
        "day_number": 1,
        "focus_module": "Exact Topic / Module Name from Context",
        "difficulty": "Beginner | Intermediate | Advanced",
        "tasks": [
          "📖 [Theory] Study specific concept [Name from notes] and key properties",
          "🛠️ [Practice] Work through practice problems on [Topic from notes]",
          "🧠 [Recall] Test active recall using ELI10 mode on [Concept from notes]"
        ],
        "estimated_time_minutes": 120,
        "checkpoint": "Master [Exact Concept Name from notes]",
        "spaced_review_topic": "None (Day 1 Kickoff)"
      }}
    ]
  }}
}}

UPLOADED SYLLABUS / NOTES CONTEXT:
{context}

JSON OUTPUT:"""


class StudyPlanner:
    """
    Intelligent Parameter-Driven Study Planner and Syllabus Topic Sequencer.
    Supports multi-factor personalization, spaced repetition intervals,
    adaptive re-balancing, iCalendar (.ics) exports, and structured study guides.
    """

    STRATEGY_DESCRIPTIONS = {
        "balanced": "Balanced Mastery — Steady pacing balancing foundational theory, problem solving, and conceptual check-ins.",
        "exam_sprint": "Exam Sprint / Cramming — High-yield focus on core testable formulas, edge cases, and aggressive active recall.",
        "deep_dive": "Deep Conceptual Dive — Thorough derivations, historical context, rigorous architectural mechanics, and extensive exercises.",
        "spaced_repetition": "Spaced Repetition & Revision — Systematically includes 1-day, 3-day, and 7-day memory retention review loops of past topics."
    }

    LEVEL_DESCRIPTIONS = {
        "beginner": "Beginner — Emphasizes gentle introductions, step-by-step breakdowns, and intuitive analogies before complex formulas.",
        "intermediate": "Intermediate — Assumes core prerequisite familiarity; focuses on standard curriculum depth and problem drills.",
        "advanced": "Advanced / Revision — Accelerates through basic definitions directly into challenging edge cases, proofs, and synthesis."
    }

    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def generate_personalized_plan(
        self,
        context_text: str,
        days: int = 7,
        hours_per_day: float = 2.0,
        study_strategy: str = "balanced",
        student_level: str = "intermediate",
        include_rest_days: bool = False,
        start_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generates a 100% syllabus-accurate personalized schedule directly from uploaded text,
        tailored by timeline constraints, daily bandwidth, learning strategy, and skill level.
        """
        if not context_text or not context_text.strip():
            context_text = "General Academic Study Materials and Course Curriculum"

        strategy_key = study_strategy.lower() if study_strategy.lower() in self.STRATEGY_DESCRIPTIONS else "balanced"
        level_key = student_level.lower() if student_level.lower() in self.LEVEL_DESCRIPTIONS else "intermediate"

        strategy_desc = self.STRATEGY_DESCRIPTIONS[strategy_key]
        level_desc = self.LEVEL_DESCRIPTIONS[level_key]

        prompt = COMPREHENSIVE_SCHEDULE_PROMPT.format(
            days=days,
            hours_per_day=hours_per_day,
            strategy=strategy_key,
            strategy_desc=strategy_desc,
            level=level_key,
            level_desc=level_desc,
            context=context_text[:14000]
        )

        raw_response = self.llm.generate(prompt=prompt, system_mode="plan_json", max_tokens=2200)
        parsed_data = self._clean_and_parse_json(raw_response)

        # Validate structured response
        if (
            parsed_data and
            isinstance(parsed_data, dict) and
            "schedule" in parsed_data and
            "days" in parsed_data["schedule"] and
            len(parsed_data["schedule"]["days"]) > 0
        ):
            modules_structure = {
                "course_title": parsed_data.get("course_title", "Course Syllabus"),
                "study_strategy": strategy_key,
                "student_level": level_key,
                "modules": parsed_data.get("modules", [])
            }
            schedule = parsed_data["schedule"]
            schedule["study_strategy"] = strategy_key
            schedule["student_level"] = level_key
            schedule["start_date"] = start_date or datetime.date.today().isoformat()

            # Ensure all required day fields exist
            for idx, d in enumerate(schedule.get("days", [])):
                if "completed" not in d:
                    d["completed"] = False
                if "day_number" not in d:
                    d["day_number"] = idx + 1
                if "estimated_time_minutes" not in d:
                    d["estimated_time_minutes"] = int(hours_per_day * 60)

            return {
                "modules_structure": modules_structure,
                "schedule": schedule
            }

        # Dynamic fallback: parse headings and topics directly from text with high fidelity
        return self._build_dynamic_plan_from_text(
            text=context_text,
            days=days,
            hours_per_day=hours_per_day,
            study_strategy=strategy_key,
            student_level=level_key,
            include_rest_days=include_rest_days,
            start_date=start_date
        )

    def rebalance_schedule(
        self,
        current_plan: Dict[str, Any],
        completed_days: Optional[List[int]] = None,
        new_target_days: Optional[int] = None,
        new_hours_per_day: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Dynamically adapts an ongoing study plan. Redistributes unfinished topic milestones
        across the newly specified remaining timeline and bandwidth.
        """
        if not current_plan or "schedule" not in current_plan:
            return current_plan

        sched = current_plan["schedule"]
        all_days = sched.get("days", [])
        
        # Determine completed vs remaining
        if completed_days is None:
            completed_days = [d["day_number"] for d in all_days if d.get("completed", False)]

        completed_items = [d for d in all_days if d["day_number"] in completed_days]
        unfinished_items = [d for d in all_days if d["day_number"] not in completed_days]

        if not unfinished_items:
            # All done!
            return current_plan

        target_remaining_days = new_target_days if new_target_days and new_target_days > 0 else len(unfinished_items)
        hours = new_hours_per_day if new_hours_per_day and new_hours_per_day > 0 else sched.get("hours_per_day", 2.0)
        minutes_per_day = int(hours * 60)

        new_days_list = list(completed_items)
        next_day_num = len(completed_items) + 1

        # Redistribute unfinished topics
        num_unfinished = len(unfinished_items)
        for i in range(target_remaining_days):
            curr_num = next_day_num + i
            topic_idx = min(int((i / max(1, target_remaining_days)) * num_unfinished), num_unfinished - 1)
            source_day = unfinished_items[topic_idx]

            new_days_list.append({
                "day_number": curr_num,
                "focus_module": source_day.get("focus_module", f"Topic Unit {curr_num}"),
                "difficulty": source_day.get("difficulty", "Intermediate"),
                "tasks": source_day.get("tasks", [
                    f"📖 [Theory] Complete core syllabus readings for {source_day.get('focus_module', 'Module')}",
                    f"🛠️ [Practice] Implement exercises and review practical examples",
                    f"🧠 [Recall] Test mastery using active recall quiz arena"
                ]),
                "estimated_time_minutes": minutes_per_day,
                "checkpoint": source_day.get("checkpoint", f"Master {source_day.get('focus_module', 'Topic')}"),
                "spaced_review_topic": f"Quick recap of Day {max(1, curr_num - 2)} key definitions" if curr_num > 2 else "None",
                "completed": False,
                "rebalanced": True
            })

        rebalanced_plan = {
            "modules_structure": current_plan.get("modules_structure", {}),
            "schedule": {
                "plan_title": f"Rebalanced {len(new_days_list)}-Day Study Plan ({hours} hrs/day)",
                "total_days": len(new_days_list),
                "hours_per_day": hours,
                "study_strategy": sched.get("study_strategy", "balanced"),
                "student_level": sched.get("student_level", "intermediate"),
                "start_date": sched.get("start_date", datetime.date.today().isoformat()),
                "days": new_days_list
            }
        }
        return rebalanced_plan

    def export_to_ics(
        self,
        plan: Dict[str, Any],
        start_date: Optional[str] = None,
        study_time_str: str = "18:00"
    ) -> str:
        """
        Generates RFC 5545 compliant iCalendar (.ics) string to import study sessions
        into Google Calendar, Apple Calendar, or Microsoft Outlook.
        """
        if not plan or "schedule" not in plan:
            return ""

        sched = plan["schedule"]
        course_title = plan.get("modules_structure", {}).get("course_title", "AI Study Buddy Course")
        days_list = sched.get("days", [])

        # Parse start date
        try:
            if start_date:
                base_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            elif sched.get("start_date"):
                base_date = datetime.datetime.strptime(sched["start_date"], "%Y-%m-%d").date()
            else:
                base_date = datetime.date.today()
        except Exception:
            base_date = datetime.date.today()

        # Parse start hour/minute
        try:
            hour, minute = map(int, study_time_str.split(":"))
        except Exception:
            hour, minute = 18, 0

        now_stamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        ics_lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//AI Study Buddy//Personalized Study Scheduler//EN",
            "CALSCALE:GREGORIAN",
            "METHOD:PUBLISH",
            f"X-WR-CALNAME:Study Plan - {course_title}",
            "X-WR-TIMEZONE:UTC"
        ]

        for idx, d in enumerate(days_list):
            d_num = d.get("day_number", idx + 1)
            event_date = base_date + datetime.timedelta(days=idx)
            start_dt = datetime.datetime(event_date.year, event_date.month, event_date.day, hour, minute)
            duration_mins = d.get("estimated_time_minutes", 120)
            end_dt = start_dt + datetime.timedelta(minutes=duration_mins)

            dt_start_str = start_dt.strftime("%Y%m%dT%H%M%S")
            dt_end_str = end_dt.strftime("%Y%m%dT%H%M%S")

            tasks_text = "\\n".join([f"• {t}" for t in d.get("tasks", [])])
            checkpoint = d.get("checkpoint", "Milestone Review")
            focus = d.get("focus_module", f"Day {d_num} Study Session")

            description = f"Course: {course_title}\\n\\n🎯 Target Milestone:\\n{checkpoint}\\n\\n📝 Action Tasks:\\n{tasks_text}"

            ics_lines.extend([
                "BEGIN:VEVENT",
                f"UID:ai-study-buddy-day-{d_num}-{now_stamp}@studyscheduler.local",
                f"DTSTAMP:{now_stamp}",
                f"DTSTART:{dt_start_str}",
                f"DTEND:{dt_end_str}",
                f"SUMMARY:📚 Day {d_num}: {focus}",
                f"DESCRIPTION:{description}",
                "STATUS:CONFIRMED",
                "BEGIN:VALARM",
                "TRIGGER:-PT15M",
                "ACTION:DISPLAY",
                f"DESCRIPTION:Reminder: Study Session - Day {d_num}: {focus}",
                "END:VALARM",
                "END:VEVENT"
            ])

        ics_lines.append("END:VCALENDAR")
        return "\r\n".join(ics_lines)

    def export_to_markdown(self, plan: Dict[str, Any]) -> str:
        """
        Exports the entire personalized study schedule as a clean, printable Markdown study guide.
        """
        if not plan or "schedule" not in plan:
            return "# No Active Study Plan\nPlease generate a plan first."

        sched = plan["schedule"]
        modules_info = plan.get("modules_structure", {})
        course_title = modules_info.get("course_title", "Course Syllabus")
        strategy = sched.get("study_strategy", "balanced").replace("_", " ").title()
        level = sched.get("student_level", "intermediate").title()

        md_lines = [
            f"# 📅 Study Roadmap: {course_title}",
            f"> **Plan Type:** {strategy} | **Level:** {level} | **Load:** {sched.get('total_days', 7)} Days @ {sched.get('hours_per_day', 2.0)} hrs/day",
            "",
            "## 🗂️ Course Modules Overview",
            "| Module # | Module Title | Difficulty | Est. Hours | Key Topics |",
            "|---|---|---|---|---|"
        ]

        for m in modules_info.get("modules", []):
            topics_str = ", ".join(m.get("topics", []))
            md_lines.append(f"| {m.get('module_number', 1)} | **{m.get('module_name')}** | `{m.get('difficulty', 'Intermediate')}` | ~{m.get('estimated_hours', 4)}h | {topics_str} |")

        md_lines.extend([
            "",
            "---",
            "",
            "## 🗓️ Day-by-Day Study Schedule & Checkpoints",
            ""
        ])

        for d in sched.get("days", []):
            d_num = d.get("day_number")
            status = "✅ Completed" if d.get("completed", False) else "⏳ Pending"
            md_lines.extend([
                f"### 📌 Day {d_num}: {d.get('focus_module')} ({d.get('estimated_time_minutes', 120)} mins) — *[{status}]*",
                f"- **🎯 Milestone Checkpoint:** `{d.get('checkpoint')}`",
                f"- **🔄 Spaced Repetition Loop:** *{d.get('spaced_review_topic', 'None')}*",
                "- **📝 Daily Action Items:**"
            ])
            for t in d.get("tasks", []):
                md_lines.append(f"  - [ ] {t}")
            md_lines.append("")

        return "\n".join(md_lines)

    def get_plan_analytics(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates study statistics and progress metrics from the current plan.
        """
        if not plan or "schedule" not in plan:
            return {
                "total_days": 0,
                "completed_days": 0,
                "completion_pct": 0.0,
                "total_hours": 0.0,
                "completed_hours": 0.0,
                "total_tasks": 0,
                "strategy": "balanced"
            }

        sched = plan["schedule"]
        days = sched.get("days", [])
        total_days = len(days)
        completed_days = sum(1 for d in days if d.get("completed", False))

        total_minutes = sum(d.get("estimated_time_minutes", 120) for d in days)
        completed_minutes = sum(d.get("estimated_time_minutes", 120) for d in days if d.get("completed", False))

        total_tasks = sum(len(d.get("tasks", [])) for d in days)

        return {
            "total_days": total_days,
            "completed_days": completed_days,
            "completion_pct": round((completed_days / max(1, total_days)) * 100, 1),
            "total_hours": round(total_minutes / 60.0, 1),
            "completed_hours": round(completed_minutes / 60.0, 1),
            "remaining_hours": round((total_minutes - completed_minutes) / 60.0, 1),
            "total_tasks": total_tasks,
            "strategy": sched.get("study_strategy", "balanced"),
            "level": sched.get("student_level", "intermediate")
        }

    def _clean_and_parse_json(self, text: str) -> Optional[Dict[str, Any]]:
        """Parses JSON safely from LLM response."""
        if not text:
            return None
        cleaned = re.sub(r'^```(?:json)?\s*', '', text.strip(), flags=re.MULTILINE)
        cleaned = re.sub(r'```\s*$', '', cleaned, flags=re.MULTILINE).strip()
        try:
            return json.loads(cleaned)
        except Exception:
            match = re.search(r'(\{[\s\S]*\})', text)
            if match:
                try:
                    return json.loads(match.group(1))
                except Exception:
                    pass
        return None

    def _build_dynamic_plan_from_text(
        self,
        text: str,
        days: int,
        hours_per_day: float,
        study_strategy: str = "balanced",
        student_level: str = "intermediate",
        include_rest_days: bool = False,
        start_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Dynamically parses headings and bullet lines from the uploaded notes
        so that every day references the EXACT terms in the user's document,
        incorporating strategy and skill level sequencing.
        """
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        
        # Extract meaningful topics and headings
        extracted_topics = []
        course_name = "Uploaded Syllabus"

        for line in lines:
            if any(k in line.lower() for k in ["course:", "syllabus:", "subject:", "title:"]):
                course_name = line.strip("# :*-")
                continue
            cleaned = re.sub(r'^[\s\-*•#0-9.:)]+', '', line).strip()
            if len(cleaned) > 5 and not cleaned.startswith("---") and not cleaned.startswith("[Source:"):
                extracted_topics.append(cleaned[:90])

        if not extracted_topics:
            extracted_topics = [
                "Core Syllabus Foundations & Definitions",
                "Key Algorithms, Proofs & Mechanisms",
                "Practical Problem Solving & Implementation",
                "Advanced Edge Cases & Optimizations",
                "Comprehensive Syllabus Active Recall"
            ]

        # Build structured modules
        num_mods = min(4, max(1, len(extracted_topics)))
        chunk_size = max(1, len(extracted_topics) // num_mods)
        modules = []
        
        difficulties = ["Beginner", "Intermediate", "Advanced", "Advanced"] if student_level != "advanced" else ["Intermediate", "Advanced", "Advanced", "Mastery"]

        for i in range(num_mods):
            mod_topics = extracted_topics[i*chunk_size : (i+1)*chunk_size]
            if not mod_topics:
                mod_topics = [extracted_topics[0]]
            
            title_topic = mod_topics[0]
            if len(title_topic) > 35:
                title_topic = title_topic[:35].rstrip(",;:- ") + "..."

            modules.append({
                "module_number": i + 1,
                "module_name": f"Module {i+1}: {title_topic}",
                "difficulty": difficulties[min(i, len(difficulties) - 1)],
                "estimated_hours": max(2, int((days * hours_per_day) / num_mods)),
                "topics": mod_topics[:4]
            })

        # Build day-by-day schedule mapping to actual extracted topics
        days_list = []
        minutes_per_day = int(hours_per_day * 60)

        def clean_topic_display(t_str: str, max_c: int = 75) -> str:
            s = t_str.strip().rstrip(" ,;:.-")
            if len(s) <= max_c:
                return s
            clipped = s[:max_c]
            last_sp = clipped.rfind(" ")
            if last_sp > 15:
                return clipped[:last_sp].rstrip(" ,;:.-")
            return clipped.rstrip(" ,;:.-")

        for d in range(1, days + 1):
            if d == days:
                # Final Day: Comprehensive Review & Quiz Drills
                days_list.append({
                    "day_number": d,
                    "focus_module": "Final Comprehensive Syllabus Review & Mock Drills",
                    "difficulty": "Advanced",
                    "tasks": [
                        "📖 [Theory] Rapid review of summary notes and core formulas across all modules",
                        "🛠️ [Practice] Work through high-yield edge case problems and past questions",
                        "🧠 [Recall] Launch 2 full-length active recall drills in the AI Quiz Arena"
                    ],
                    "estimated_time_minutes": minutes_per_day,
                    "checkpoint": "Complete Full Syllabus Exam Readiness",
                    "spaced_review_topic": "All Module Core Formulas",
                    "completed": False
                })
            elif include_rest_days and d % 7 == 0:
                # Periodic Spaced Repetition / Buffer Day
                days_list.append({
                    "day_number": d,
                    "focus_module": f"Spaced Review & Buffer Checkpoint (Week {d//7})",
                    "difficulty": "Intermediate",
                    "tasks": [
                        f"🧠 [Recall] Active recall flashcard session reviewing Days 1 to {d-1}",
                        "🛠️ [Practice] Re-attempt any difficult practice problems from earlier units",
                        "💬 [Tutor] Clarify any conceptual doubts using Strict Syllabus Tutor"
                    ],
                    "estimated_time_minutes": minutes_per_day,
                    "checkpoint": f"Solidify Memory Retention for Weeks 1-{d//7}",
                    "spaced_review_topic": f"Topics from Days {max(1, d-6)} to {d-1}",
                    "completed": False
                })
            else:
                idx = int(((d - 1) / max(1, days - 1)) * len(extracted_topics))
                topic = extracted_topics[min(idx, len(extracted_topics) - 1)]
                clean_t = clean_topic_display(topic, 75)
                
                # Determine past topic for spaced review
                if d == 1:
                    spaced_note = "None (Day 1 Kickoff)"
                elif d == 2:
                    spaced_note = f"Review Day 1: {clean_topic_display(extracted_topics[0], 40)}"
                else:
                    prev_idx = max(0, idx - 1)
                    spaced_note = f"10m Recall on Day {d-1}: {clean_topic_display(extracted_topics[prev_idx], 40)}"

                if study_strategy == "exam_sprint":
                    tasks = [
                        f"📖 [High-Yield Theory] Extract key testable definitions and theorems for {clean_t}",
                        f"🛠️ [Speed Drills] Solve high-probability exam questions on {clean_t}",
                        f"🧠 [Active Recall] Complete active recall test in Kahoot Quiz Arena"
                    ]
                elif study_strategy == "deep_dive":
                    tasks = [
                        f"📖 [Deep Theory] Understand theoretical foundations & architectural proofs of {clean_t}",
                        f"🛠️ [Implementation] Step-by-step practical derivation / problem analysis for {clean_t}",
                        f"🧠 [Synthesis] Teach concept in ELI10 mode to verify 100% intuition"
                    ]
                elif study_strategy == "spaced_repetition":
                    tasks = [
                        f"🧠 [15m Spaced Recall] Quick recall review: {spaced_note}",
                        f"📖 [New Concept] Study core mechanisms & properties of {clean_t}",
                        f"🛠️ [Application] Solve targeted practical exercises on {clean_t}"
                    ]
                else:  # balanced
                    tasks = [
                        f"📖 [Theory] Core definitions and foundations of {clean_t}",
                        f"🛠️ [Practice] Practical exercises and problems on {clean_t}",
                        f"🧠 [Recall] Active recall check on {clean_t}"
                    ]

                days_list.append({
                    "day_number": d,
                    "focus_module": clean_t,
                    "difficulty": "Beginner" if d <= 2 and student_level == "beginner" else "Intermediate",
                    "tasks": tasks,
                    "estimated_time_minutes": minutes_per_day,
                    "checkpoint": f"Master {clean_t}",
                    "spaced_review_topic": spaced_note,
                    "completed": False
                })

        return {
            "modules_structure": {
                "course_title": course_name,
                "study_strategy": study_strategy,
                "student_level": student_level,
                "modules": modules
            },
            "schedule": {
                "plan_title": f"Personalized {days}-Day Study Plan ({hours_per_day} hrs/day)",
                "total_days": days,
                "hours_per_day": hours_per_day,
                "study_strategy": study_strategy,
                "student_level": student_level,
                "start_date": start_date or datetime.date.today().isoformat(),
                "days": days_list
            }
        }
