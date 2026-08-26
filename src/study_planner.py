"""
Study Planner & Syllabus Analyzer
Performs deep topic extraction, prerequisite sequencing, and builds a realistic,
syllabus-specific day-by-day study schedule from the student's uploaded notes.
"""

import json
import re
from typing import Dict, Any, List, Optional
from src.llm_client import LLMClient

COMPREHENSIVE_SCHEDULE_PROMPT = """You are an expert academic curriculum designer and study schedule planner.
Analyze the following uploaded student course notes/syllabus and construct a customized, day-by-day study roadmap.

CRITICAL INSTRUCTIONS:
1. You MUST extract the REAL topics, module titles, formulas, algorithms, definitions, and mechanisms from the provided text below.
2. DO NOT use generic placeholders like "Foundations & Core Principles", "Read introductory sections", "Complete notes summary".
3. Every day MUST focus on a specific topic from the context (e.g. "Linear Regression & Overfitting", "Linked Lists & Floyd's Cycle Detection", "Glycolysis & Krebs Cycle").
4. For each day, create 3 detailed, concrete action items naming the exact concepts from the document.
5. Create a specific Target Milestone for each day reflecting the actual concept mastered.
6. Distribute the material across exactly {days} days with a target load of {hours_per_day} hours/day.
7. Return strictly a valid JSON object matching the schema below.

REQUIRED JSON SCHEMA:
{{
  "course_title": "Specific Course Title from Uploaded Context",
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
        "tasks": [
          "Study specific concept [Name from notes] and key properties",
          "Work through practice problems on [Topic from notes]",
          "Test active recall using ELI10 mode on [Concept from notes]"
        ],
        "estimated_time_minutes": 120,
        "checkpoint": "Master [Exact Concept Name from notes]"
      }}
    ]
  }}
}}

UPLOADED SYLLABUS / NOTES CONTEXT:
{context}

JSON OUTPUT:"""


class StudyPlanner:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def generate_personalized_plan(
        self,
        context_text: str,
        days: int = 7,
        hours_per_day: float = 2.0
    ) -> Dict[str, Any]:
        """
        Generates a 100% syllabus-accurate personalized schedule directly from the uploaded text.
        """
        if not context_text or not context_text.strip():
            context_text = "General Study Materials"

        prompt = COMPREHENSIVE_SCHEDULE_PROMPT.format(
            days=days,
            hours_per_day=hours_per_day,
            context=context_text[:12000]
        )

        raw_response = self.llm.generate(prompt=prompt, system_mode="plan_json", max_tokens=1800)
        parsed_data = self._clean_and_parse_json(raw_response)

        # If LLM returned valid comprehensive JSON
        if (
            parsed_data and
            isinstance(parsed_data, dict) and
            "schedule" in parsed_data and
            "days" in parsed_data["schedule"] and
            len(parsed_data["schedule"]["days"]) > 0
        ):
            modules_structure = {
                "course_title": parsed_data.get("course_title", "Course Syllabus"),
                "modules": parsed_data.get("modules", [])
            }
            schedule = parsed_data["schedule"]
            for d in schedule.get("days", []):
                if "completed" not in d:
                    d["completed"] = False
            return {
                "modules_structure": modules_structure,
                "schedule": schedule
            }

        # Dynamic fallback: parse headings and topics directly from text
        return self._build_dynamic_plan_from_text(context_text, days, hours_per_day)

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

    def _build_dynamic_plan_from_text(self, text: str, days: int, hours_per_day: float) -> Dict[str, Any]:
        """
        Dynamically parses headings and bullet lines from the uploaded notes
        so that every day references the EXACT terms in the user's document.
        """
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        
        # Extract meaningful topics and headings
        extracted_topics = []
        course_name = "Uploaded Syllabus"

        for line in lines:
            if any(k in line.lower() for k in ["course:", "syllabus:", "subject:"]):
                course_name = line.strip("# :*-")
                continue
            cleaned = line.lstrip("-*• 0123456789.:# ")
            if len(cleaned) > 10 and not cleaned.startswith("---"):
                extracted_topics.append(cleaned[:90])

        if not extracted_topics:
            extracted_topics = ["Key Principles from Notes", "Core Definitions & Methods", "Problem Solving Drills"]

        # Build modules
        chunk_size = max(1, len(extracted_topics) // 3)
        modules = []
        for i in range(min(3, max(1, len(extracted_topics)))):
            mod_topics = extracted_topics[i*chunk_size : (i+1)*chunk_size]
            if not mod_topics:
                mod_topics = [extracted_topics[0]]
            modules.append({
                "module_number": i + 1,
                "module_name": f"Module {i+1}: {mod_topics[0][:40]}",
                "difficulty": "Beginner" if i == 0 else ("Intermediate" if i == 1 else "Advanced"),
                "estimated_hours": max(2, int((days * hours_per_day) / 3)),
                "topics": mod_topics[:4]
            })

        # Build day-by-day schedule mapping to actual extracted topics
        days_list = []
        minutes_per_day = int(hours_per_day * 60)

        for d in range(1, days + 1):
            if d == days:
                days_list.append({
                    "day_number": d,
                    "focus_module": "Final Comprehensive Syllabus Review & Mock Drills",
                    "tasks": [
                        "Review all summary notes and core definitions across all modules",
                        "Launch 2 full-length active recall drills in the AI Quiz Arena",
                        "Clarify edge cases and tricky concepts in Strict Tutor mode"
                    ],
                    "estimated_time_minutes": minutes_per_day,
                    "checkpoint": "Complete Full Syllabus Exam Readiness",
                    "completed": False
                })
            else:
                idx = int(((d - 1) / max(1, days - 1)) * len(extracted_topics))
                topic = extracted_topics[min(idx, len(extracted_topics) - 1)]
                
                days_list.append({
                    "day_number": d,
                    "focus_module": f"Topic: {topic[:50]}",
                    "tasks": [
                        f"Study concept: {topic}",
                        f"Work through practical examples & formula sheet for {topic[:35]}",
                        f"Test conceptual mastery with ELI10 mode on {topic[:30]}"
                    ],
                    "estimated_time_minutes": minutes_per_day,
                    "checkpoint": f"Master {topic[:40]}",
                    "completed": False
                })

        return {
            "modules_structure": {
                "course_title": course_name,
                "modules": modules
            },
            "schedule": {
                "plan_title": f"Personalized {days}-Day Study Plan ({hours_per_day} hrs/day)",
                "total_days": days,
                "hours_per_day": hours_per_day,
                "days": days_list
            }
        }
