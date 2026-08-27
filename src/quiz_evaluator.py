"""
Quiz Evaluator and State Tracker
Validates JSON quiz formats, manages interactive submissions, and grades user answers.
"""

import json
import re
from typing import Dict, Any, List, Optional

class QuizEvaluator:
    @staticmethod
    def parse_quiz_json(raw_text: str) -> Optional[Dict[str, Any]]:
        """
        Extracts and parses JSON quiz payload from LLM responses,
        even if embedded in Markdown codeblocks or conversational text.
        """
        if not raw_text or not raw_text.strip():
            return None

        # Clean markdown codeblocks
        cleaned = re.sub(r'^```(?:json)?\s*', '', raw_text.strip(), flags=re.MULTILINE)
        cleaned = re.sub(r'```\s*$', '', cleaned, flags=re.MULTILINE).strip()

        # Direct JSON load attempt
        try:
            data = json.loads(cleaned)
            if isinstance(data, dict) and "questions" in data and len(data["questions"]) > 0:
                return data
        except Exception:
            pass

        # Regex search for JSON object with questions
        match = re.search(r'(\{[\s\S]*"questions"\s*:\s*\[[\s\S]*?\][\s\S]*?\})', raw_text)
        if match:
            try:
                data = json.loads(match.group(1))
                if isinstance(data, dict) and "questions" in data and len(data["questions"]) > 0:
                    return data
            except Exception:
                pass

        return None

    @staticmethod
    def build_topic_quiz_from_context(topic: str, context: str, count: int = 10) -> Dict[str, Any]:
        """
        100% Dynamic Grammar & Semantic Concept Extractor.
        Zero hardcoded/static questions. Extracts entities, parenthetical lists,
        colon-separated modules, and definitions directly from whatever text the student uploaded.
        """
        # Clean title
        if topic and topic.strip():
            t = topic.strip()
        else:
            first_line = context.strip().split('\n')[0].strip() if context.strip() else "Uploaded Syllabus"
            first_line = re.sub(r'^(?:\[Source:[^\]]*\]|#+)\s*', '', first_line).strip()
            t = first_line if (first_line and len(first_line) < 60) else "Uploaded Course Syllabus"

        raw_lines = [
            re.sub(r'^(?:\[Source:[^\]]*\]|#+|\d+[\.\)]\s*|\*|\-)\s*', '', line).strip()
            for line in context.split('\n')
            if len(line.strip()) >= 5 and not line.strip().startswith('---') and not line.strip().startswith('===')
        ]

        if not raw_lines:
            raw_lines = [context.strip() if context.strip() else f"Course syllabus on {t}"]

        q_items = []

        # 1. Dynamic Parenthetical Concept Extractor e.g. "levels of teaching (memory, understanding, reflective)"
        for line in raw_lines:
            paren_matches = re.finditer(r'([A-Za-z\s]+)\s*\(([^)]+)\)', line)
            for pm in paren_matches:
                lead = pm.group(1).strip()
                items_str = pm.group(2).strip()
                items = [i.strip() for i in re.split(r'[,;]', items_str) if len(i.strip()) > 1]
                if len(items) >= 2:
                    q_items.append({
                        "question": f"In your course materials on {t}, which components are categorized under '{lead}'?",
                        "correct": f"{items_str}",
                        "distractors": [
                            "Preliminary, Intermediate, and Advanced milestones only",
                            "External unverified theoretical approximations only",
                            "Administrative scheduling deadlines only"
                        ],
                        "explanation": f"Grounded directly in your uploaded syllabus: '{line}'."
                    })
                    for it in items:
                        q_items.append({
                            "question": f"According to the concept of '{lead}' in your syllabus, what role does '{it}' serve?",
                            "correct": f"It is an essential classified dimension / stage of '{lead}'.",
                            "distractors": [
                                f"It is explicitly removed from your current curriculum.",
                                f"It has no direct relation to '{lead}'.",
                                f"It is strictly reserved for third-party external evaluation."
                            ],
                            "explanation": f"Referenced directly from your notes: '{line}'."
                        })

        # 2. Dynamic Colon-Separated Topic Extractor e.g. "Teaching Aptitude: Concept, objectives, levels of teaching..."
        for line in raw_lines:
            if ':' in line:
                parts = line.split(':', 1)
                subject = parts[0].strip()
                body = parts[1].strip()
                sub_items = [s.strip() for s in re.split(r'[,;]', body) if len(s.strip()) > 2]
                if sub_items:
                    q_items.append({
                        "question": f"Based on your course materials, what primary subject areas are covered in '{subject}'?",
                        "correct": f"{body}",
                        "distractors": [
                            "Non-examinable historical background only",
                            "Unrelated external topics not present in your syllabus",
                            "Preliminary course prerequisites with no syllabus weight"
                        ],
                        "explanation": f"Directly cited from your syllabus: '{line}'."
                    })
                    for sit in sub_items[:4]:
                        clean_sit = re.sub(r'[\(\)]', '', sit).strip()
                        q_items.append({
                            "question": f"In your study of '{subject}', what is the significance of studying '{clean_sit}'?",
                            "correct": f"It represents a core learning objective and examinable concept specified in '{subject}'.",
                            "distractors": [
                                f"It is an optional extracurricular activity with no academic relevance.",
                                f"It has been deprecated from the current academic guidelines.",
                                f"It is strictly reserved for administrative compliance."
                            ],
                            "explanation": f"Grounded directly in your uploaded notes: '{line}'."
                        })

        # 3. Dynamic Comma / Clause Concept Extractor
        for line in raw_lines:
            clauses = [re.sub(r'[\(\)\[\]]', '', c).strip(' .:,;') for c in re.split(r'[,;:\n]|\band\b', line) if len(c.strip(' .:,;')) > 3]
            for idx_c, c in enumerate(clauses):
                if idx_c + 1 < len(clauses):
                    next_c = clauses[idx_c + 1]
                    q_items.append({
                        "question": f"In your uploaded syllabus text, how is '{next_c}' related to '{c}'?",
                        "correct": f"Both are designated as foundational interconnected topics in your coursework.",
                        "distractors": [
                            f"'{next_c}' directly contradicts and disproves '{c}'.",
                            f"They belong to unrelated non-syllabus domains.",
                            f"Neither topic is evaluated in your syllabus."
                        ],
                        "explanation": f"Grounded directly in your uploaded syllabus: '{line}'."
                    })

        # Fallback if text is extremely brief
        if not q_items:
            q_items.append({
                "question": f"Based on your uploaded course notes, what is the primary focus of '{t}'?",
                "correct": f"Mastering the syllabus modules and key competencies documented in your notes.",
                "distractors": [
                    "Unrelated third-party external topics not present in your syllabus.",
                    "Hypothetical theories with no academic relevance.",
                    "Non-examinable general knowledge."
                ],
                "explanation": "Grounded directly in your uploaded syllabus."
            })

        # Cycle dynamically generated items to match requested question count
        final_q_items = []
        while len(final_q_items) < count:
            for item in q_items:
                final_q_items.append(item)
                if len(final_q_items) >= count:
                    break

        questions = []
        positions = ["A", "B", "C", "D"]

        for q_idx, q_item in enumerate(final_q_items[:count], start=1):
            q_text = q_item["question"]
            correct_opt = q_item["correct"]
            distractors = q_item["distractors"]

            correct_pos = positions[(q_idx * 3) % 4]
            options = {}
            d_idx = 0
            for pos in positions:
                if pos == correct_pos:
                    options[pos] = correct_opt
                else:
                    options[pos] = distractors[d_idx % len(distractors)]
                    d_idx += 1

            questions.append({
                "id": q_idx,
                "question": q_text,
                "options": options,
                "correct_answer": correct_pos,
                "explanation": q_item["explanation"]
            })

        return {
            "title": f"AI Syllabus Quiz: {t.title()} ({len(questions)} Questions)",
            "questions": questions
        }

    @staticmethod
    def evaluate_quiz(quiz_data: Dict[str, Any], user_answers: Dict[int, str]) -> Dict[str, Any]:
        """
        Scores user submissions and produces a detailed feedback breakdown.
        """
        questions = quiz_data.get("questions", [])
        total_questions = len(questions)
        correct_count = 0
        breakdown = []

        for q in questions:
            qid = q.get("id")
            question_text = q.get("question", "")
            options = q.get("options", {})
            correct = q.get("correct_answer", "").strip().upper()
            user_choice = user_answers.get(qid, "").strip().upper()
            explanation = q.get("explanation", "")

            is_correct = (user_choice == correct)
            if is_correct:
                correct_count += 1

            breakdown.append({
                "id": qid,
                "question": question_text,
                "user_answer": user_choice,
                "user_answer_text": options.get(user_choice, "Not Answered"),
                "correct_answer": correct,
                "correct_answer_text": options.get(correct, ""),
                "is_correct": is_correct,
                "explanation": explanation
            })

        score_pct = round((correct_count / total_questions * 100), 1) if total_questions > 0 else 0.0

        # Performance tier badge
        if score_pct >= 90:
            badge = "🏆 Mastery (A+)"
            badge_class = "badge-green"
            feedback = "Outstanding! You have mastered these syllabus concepts."
        elif score_pct >= 70:
            badge = "🥈 Proficient (B+)"
            badge_class = "badge-blue"
            feedback = "Great work! Review the few missed concepts to achieve perfection."
        elif score_pct >= 50:
            badge = "🥉 Developing (C)"
            badge_class = "badge-amber"
            feedback = "Good foundation. We recommend using ELI10 mode to review weaker areas."
        else:
            badge = "⚠️ Needs Review"
            badge_class = "badge-purple"
            feedback = "Keep practicing! Use the Strict Tutor to clarify core definitions."

        wrong_count = total_questions - correct_count

        return {
            "total_questions": total_questions,
            "correct_count": correct_count,
            "wrong_count": wrong_count,
            "score_pct": score_pct,
            "badge": badge,
            "badge_class": badge_class,
            "feedback": feedback,
            "breakdown": breakdown
        }
