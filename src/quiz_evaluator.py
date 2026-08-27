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
        Dynamically synthesizes 100% custom multiple-choice questions extracted
        in real time from the specific sentences, clauses, and concepts of the uploaded document.
        Zero hardcoded or static question banks.
        """
        # Extract dynamic topic title
        if topic and topic.strip():
            t = topic.strip()
        else:
            first_line = context.strip().split('\n')[0].strip() if context.strip() else "Uploaded Syllabus"
            first_line = re.sub(r'^(?:\[Source:[^\]]*\]|#+)\s*', '', first_line).strip()
            t = first_line if (first_line and len(first_line) < 60) else "Uploaded Course Syllabus"

        # 1. Clean and extract distinct meaningful lines from the uploaded document
        raw_lines = [
            re.sub(r'^(?:\[Source:[^\]]*\]|#+|\d+[\.\)]\s*|\*|\-)\s*', '', line).strip()
            for line in context.split('\n')
            if len(line.strip()) >= 15 and not line.strip().startswith('---') and not line.strip().startswith('===')
        ]

        if not raw_lines:
            raw_lines = [context.strip() if context.strip() else f"Course curriculum on {t}"]

        # 2. Extract atomic concepts, terms, and clauses
        all_concepts = []
        for line in raw_lines:
            # Split by commas, semicolons, colons, or parentheses
            clauses = [re.sub(r'[\(\)\[\]]', '', c).strip(' .:,;') for c in re.split(r'[,;:\n]|\band\b', line) if len(c.strip(' .:,;')) > 3]
            for c in clauses:
                if len(c) >= 3 and c.lower() not in [x.lower() for x in all_concepts]:
                    all_concepts.append(c)

        if not all_concepts:
            all_concepts = [t, "Foundational Principles", "Core Syllabus Concepts", "Course Modules"]

        # 3. Dynamically synthesize questions for each line/concept
        q_items = []
        for idx, line in enumerate(raw_lines):
            clauses = [re.sub(r'[\(\)\[\]]', '', c).strip(' .:,;') for c in re.split(r'[,;:\n]|\band\b', line) if len(c.strip(' .:,;')) > 3]
            main_term = clauses[0] if clauses else f"Module {idx+1}"
            related_terms = clauses[1:] if len(clauses) > 1 else [f"Systematic study of {main_term}"]

            # Template Type 1: Core Focus
            q_items.append({
                "question": f"According to your uploaded document, which of the following is an essential topic covered under '{main_term}'?",
                "correct": f"{', '.join(related_terms[:3]) if related_terms else main_term}",
                "distractors": [
                    f"This subject is explicitly omitted from your coursework.",
                    f"Only applies as an external unverified hypothesis.",
                    f"Replaced entirely by non-examinable background reading."
                ],
                "explanation": f"Grounded directly in your uploaded syllabus: '{line}'."
            })

            # Template Type 2: Conceptual Scope
            if len(clauses) > 1:
                target_term = clauses[1]
                q_items.append({
                    "question": f"In your course curriculum on '{t}', what role does '{target_term}' play in relation to '{main_term}'?",
                    "correct": f"It is a core component and learning requirement specified alongside '{main_term}'.",
                    "distractors": [
                        f"It is defined as an obsolete concept no longer evaluated.",
                        f"It operates independently without any connection to '{main_term}'.",
                        f"It is solely used for administrative scheduling with no academic content."
                    ],
                    "explanation": f"Referenced directly from your notes: '{line}'."
                })

            # Template Type 3: Factual Verification
            q_items.append({
                "question": f"Which of the following statements is TRUE regarding the syllabus requirements for '{main_term}'?",
                "correct": f"Students must study and master: {line}.",
                "distractors": [
                    f"Students are only required to memorize historical trivia without applying '{main_term}'.",
                    f"The module on '{main_term}' has been removed from the current term's evaluation.",
                    f"It strictly forbids practical exercises or conceptual definitions."
                ],
                "explanation": f"Directly cited from your uploaded text: '{line}'."
            })

        # Ensure we have enough dynamic items to satisfy the requested question count
        if not q_items:
            q_items.append({
                "question": f"Based on your uploaded course notes, what is the primary focus of '{t}'?",
                "correct": f"Mastering the syllabus modules and key objectives documented in your notes.",
                "distractors": [
                    f"Unrelated third-party external topics not present in your syllabus.",
                    f"Hypothetical theories with no academic relevance.",
                    f"Non-examinable general knowledge."
                ],
                "explanation": f"Grounded directly in your uploaded syllabus."
            })

        # Cycle dynamically generated items
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
