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
    def get_daily_smart_reminder() -> Dict[str, str]:
        """Returns a motivating smart reminder for the student dashboard."""
        return random.choice(MOTIVATIONAL_QUOTES)
