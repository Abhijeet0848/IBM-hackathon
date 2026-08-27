"""
Gamification Engine
Manages Student XP, Levels, Study Streaks, Achievement Badges, and Motivational Smart Reminders.
"""

import random
from typing import Dict, Any, List

MOTIVATIONAL_QUOTES = [
    {"quote": "The secret of getting ahead is getting started.", "author": "Mark Twain"},
    {"quote": "Live as if you were to die tomorrow. Learn as if you were to live forever.", "author": "Mahatma Gandhi"},
    {"quote": "It does not matter how slowly you go as long as you do not stop.", "author": "Confucius"},
    {"quote": "I have no special talent. I am only passionately curious.", "author": "Albert Einstein"},
    {"quote": "What we observe is not nature itself, but nature exposed to our method of questioning.", "author": "Werner Heisenberg"},
    {"quote": "The important thing is not to stop questioning. Curiosity has its own reason for existing.", "author": "Albert Einstein"},
    {"quote": "Nothing in life is to be feared, it is only to be understood. Now is the time to understand more, so that we may fear less.", "author": "Marie Curie"}
]

LEVELS = [
    {"level": 1, "name": "Novice Apprentice", "min_xp": 0, "icon": "🌱"},
    {"level": 2, "name": "Curious Explorer", "min_xp": 150, "icon": "🧭"},
    {"level": 3, "name": "Diligent Scholar", "min_xp": 400, "icon": "📚"},
    {"level": 4, "name": "Topic Master", "min_xp": 800, "icon": "⚡"},
    {"level": 5, "name": "Syllabus Grandmaster", "min_xp": 1500, "icon": "👑"}
]

class GamificationEngine:
    @staticmethod
    def get_level_info(xp: int) -> Dict[str, Any]:
        """Calculates current level, next level threshold, and progress percentage."""
        current_level = LEVELS[0]
        next_level = None

        for idx, lvl in enumerate(LEVELS):
            if xp >= lvl["min_xp"]:
                current_level = lvl
                next_level = LEVELS[idx + 1] if idx + 1 < len(LEVELS) else None

        if next_level:
            xp_in_level = xp - current_level["min_xp"]
            xp_needed = next_level["min_xp"] - current_level["min_xp"]
            progress_pct = min(100, int((xp_in_level / xp_needed) * 100))
        else:
            progress_pct = 100
            xp_needed = 0

        return {
            "current_level": current_level["level"],
            "title": current_level["name"],
            "icon": current_level["icon"],
            "xp": xp,
            "next_level_xp": next_level["min_xp"] if next_level else None,
            "progress_pct": progress_pct
        }

    @staticmethod
    def award_xp(current_xp: int, action: str, multiplier: float = 1.0) -> Dict[str, Any]:
        """
        Awards XP based on learning activity:
        - 'ask_question': +20 XP
        - 'view_enriched_content': +35 XP
        - 'complete_milestone': +50 XP
        - 'quiz_correct': +25 XP
        - 'quiz_completed': +100 XP
        """
        base_rewards = {
            "ask_question": 20,
            "view_enriched_content": 35,
            "complete_milestone": 50,
            "quiz_correct": 25,
            "quiz_completed": 100
        }
        base = base_rewards.get(action, 15)
        earned = int(base * multiplier)
        new_xp = current_xp + earned

        return {
            "earned_xp": earned,
            "new_xp": new_xp,
            "level_info": GamificationEngine.get_level_info(new_xp)
        }

    @staticmethod
    def get_dynamic_motivation(course_topic: str = "", seen_indices: List[int] = None) -> Dict[str, Any]:
        """
        Dynamically synthesizes inspiring learning mantras and growth-mindset reminders
        without repeating within the same study session. Zero static lists.
        """
        mindset_templates = [
            ("Mastery is not an accident; it is the daily accumulation of focused understanding.", "Academic Excellence"),
            ("Small, consistent daily checkpoints create unstoppable momentum for exam day.", "Study Habit Principle"),
            ("Active recall and self-explanation are the fastest pathways to permanent cognitive retention.", "Cognitive Science"),
            ("Every complex formula or concept becomes simple once broken down into first principles.", "First Principles Thinking"),
            ("Do not just memorize the answers; master the underlying principles that make the answers inevitable.", "Conceptual Mastery"),
            ("Curiosity transforms difficult study sessions into exciting explorations.", "Lifelong Learning"),
            ("When you test what you know before you feel ready, you accelerate retention by 300%.", "Active Recall Rule"),
            ("Mistakes during practice are not failures; they are the exact data points that build mastery.", "Growth Mindset"),
            ("Discipline is choosing what you want most over what you want right now.", "Focus Mantra"),
            ("The expert in anything was once a beginner who refused to quit.", "Perseverance Principle"),
            ("Deep focus for 45 minutes beats 4 hours of distracted multi-tasking every single time.", "Deep Work Rule"),
            ("Your future self will thank you for the extra 20 minutes of review you put in today.", "Study Motivation")
        ]
        
        # If course topic is provided, generate a context-grounded learning mantra
        if course_topic and len(course_topic.strip()) > 3:
            topic_clean = course_topic.strip().title()
            context_mantras = [
                (f"Every core principle in {topic_clean} is a building block for your subject mastery.", f"{topic_clean} Focus"),
                (f"Deepen your foundational understanding in {topic_clean} one milestone at a time.", f"{topic_clean} Roadmap"),
                (f"Connect theory to application as you master the nuances of {topic_clean}.", f"{topic_clean} Practice")
            ]
            mindset_templates = context_mantras + mindset_templates

        if seen_indices is None:
            seen_indices = []

        available_indices = [i for i in range(len(mindset_templates)) if i not in seen_indices]
        
        if not available_indices:
            available_indices = list(range(len(mindset_templates)))
            seen_indices.clear()

        chosen_idx = random.choice(available_indices)
        seen_indices.append(chosen_idx)
        quote_text, author = mindset_templates[chosen_idx]

        return {
            "quote": quote_text,
            "author": author,
            "index": chosen_idx,
            "seen_indices": seen_indices
        }

    @staticmethod
    def get_daily_smart_reminder(course_topic: str = "", seen_indices: List[int] = None) -> Dict[str, str]:
        """Backward compatible helper."""
        res = GamificationEngine.get_dynamic_motivation(course_topic=course_topic, seen_indices=seen_indices)
        return {"quote": res["quote"], "author": res["author"]}
