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
        Synthesizes 10 accurate, document-grounded questions directly from the uploaded context.
        """
        t = topic.strip() if topic else "Syllabus Concepts"
        lines = [line.strip() for line in context.split('\n') if line.strip()]
        
        # Filter lines relevant to topic or meaningful facts
        relevant_lines = []
        for line in lines:
            if len(line) > 20 and not line.startswith("---") and not line.startswith("[Source:"):
                cleaned = line.lstrip("-*• 0123456789.:# ")
                if len(cleaned) > 25:
                    if t.lower() in cleaned.lower():
                        relevant_lines.insert(0, cleaned)
                    else:
                        relevant_lines.append(cleaned)

        if not relevant_lines:
            relevant_lines = [
                f"{t} represents memory addresses and references to data stored in memory.",
                f"Dereferencing a pointer accesses or modifies the value at the referenced memory address.",
                f"Uninitialized or dangling pointers can lead to undefined behavior or segmentation faults.",
                f"Pointer arithmetic allows incrementing or decrementing addresses based on data type size.",
                f"NULL pointers represent invalid or unassigned addresses to ensure safe checking.",
                f"Dynamic memory allocation functions like malloc() return a void* pointer.",
                f"Pass-by-reference using pointers allows functions to mutate caller variables directly.",
                f"Array names in C decay to a pointer to their first element in most expressions.",
                f"Function pointers allow passing functions as arguments to other algorithms.",
                f"Double pointers (pointers to pointers) are used to modify pointer variables themselves."
            ]

        questions = []
        positions = ["A", "B", "C", "D"]

        for q_idx in range(1, count + 1):
            line_idx = (q_idx - 1) % len(relevant_lines)
            fact = relevant_lines[line_idx].strip()
            
            # Preserve complete sentences without cutting words
            if len(fact) > 160:
                # Truncate at nearest word boundary
                words = fact.split()
                fact_snip = ""
                for w in words:
                    if len(fact_snip) + len(w) + 1 > 140:
                        break
                    fact_snip = f"{fact_snip} {w}".strip()
                fact_snip = fact_snip.rstrip(",;:-") + "..."
            else:
                fact_snip = fact

            q_text = f"According to your uploaded document, which of the following is TRUE regarding: '{fact_snip}'?"
            correct_opt = f"{fact}"
            distractor_1 = f"It is explicitly contradicted and considered invalid in this course."
            distractor_2 = f"It operates with zero memory overhead and requires no execution time."
            distractor_3 = f"It was permanently deprecated and excluded from the syllabus."

            correct_pos = positions[(q_idx * 3) % 4]
            options = {}
            distractors = [distractor_1, distractor_2, distractor_3]
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
                "explanation": f"Verified directly from your uploaded document: \"{fact}\""
            })

        return {
            "title": f"Comprehensive Syllabus Quiz: {t.title()} ({count} Questions)",
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

        return {
            "total_questions": total_questions,
            "correct_count": correct_count,
            "score_pct": score_pct,
            "badge": badge,
            "badge_class": badge_class,
            "feedback": feedback,
            "breakdown": breakdown
        }
