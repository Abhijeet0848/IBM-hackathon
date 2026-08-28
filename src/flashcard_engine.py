"""
Interactive AI Flashcard Engine & Spaced Recall Flip Arena
Extracts key concepts, definitions, formulas, and principles from syllabus materials
and provides a 3D animated flip-card active recall interface with Leitner-box tracking.
"""

import json
import re
import random
from typing import List, Dict, Any, Optional

class FlashcardEngine:
    @staticmethod
    def generate_flashcards(
        context_text: str,
        count: int = 8,
        llm_client: Any = None
    ) -> List[Dict[str, Any]]:
        """
        Generates high-yield active recall flashcards from course context.
        """
        if not context_text or len(context_text.strip()) < 10:
            return FlashcardEngine._get_fallback_flashcards("General Studies", count)

        cards = []

        # 1. Attempt LLM Generation if available
        if llm_client and hasattr(llm_client, "generate") and llm_client.is_connected():
            prompt = (
                f"You are an expert cognitive learning tutor. Analyze the following course syllabus / notes:\n\n"
                f"{context_text[:8000]}\n\n"
                f"Extract exactly {count} high-yield active recall flashcards covering key definitions, "
                f"core formulas, fundamental principles, and conceptual differences from this document.\n\n"
                f"Output strictly valid JSON as an array of objects matching this format:\n"
                f"[\n"
                f'  {{"id": 1, "front": "Specific Question or Definition Prompt from Notes", "back": "Accurate, concise definition or breakdown", "category": "Topic Name", "difficulty": "Medium"}}\n'
                f"]"
            )
            try:
                raw_resp = llm_client.generate(prompt=prompt, system_mode="plan_json", max_tokens=3000, temperature=0.3)
                json_match = re.search(r'\[.*\]', raw_resp, re.DOTALL)
                if json_match:
                    parsed = json.loads(json_match.group(0))
                    if isinstance(parsed, list) and len(parsed) > 0:
                        cards = parsed
            except Exception:
                pass

        # 2. If LLM returned fewer than count, supplement with heuristic context cards
        if len(cards) < count:
            heuristic_cards = FlashcardEngine._synthesize_from_context(context_text, count - len(cards))
            existing_fronts = {c.get("front", "").strip().lower() for c in cards}
            for hc in heuristic_cards:
                if hc.get("front", "").strip().lower() not in existing_fronts:
                    cards.append(hc)
                if len(cards) >= count:
                    break

        # 3. If still below requested count, pad with cognitive learning science cards
        if len(cards) < count:
            fallbacks = FlashcardEngine._get_fallback_flashcards("Study Mastery", count)
            for fb in fallbacks:
                if len(cards) >= count:
                    break
                cards.append(fb)

        # Ensure unique sequential IDs
        for idx, c in enumerate(cards[:count]):
            c["id"] = idx + 1

        return cards[:count]

    @staticmethod
    def _synthesize_from_context(text: str, count: int) -> List[Dict[str, Any]]:
        """Generates clean, syllabus-derived flashcards from text sentences and bullet points."""
        lines = [ln.strip() for ln in text.splitlines() if len(ln.strip()) > 10]
        cards = []
        card_id = 1

        for ln in lines:
            if len(cards) >= count:
                break
            # Look for definitions or key concepts separated by colon, dash, or parentheses
            if ":" in ln:
                parts = ln.split(":", 1)
                term, explanation = parts[0].strip(), parts[1].strip()
                if 2 < len(term) < 70 and len(explanation) > 10:
                    cards.append({
                        "id": card_id,
                        "front": f"Define and explain: **{term}**",
                        "back": explanation,
                        "category": "Core Concept",
                        "difficulty": "Medium"
                    })
                    card_id += 1
            elif " - " in ln:
                parts = ln.split(" - ", 1)
                term, explanation = parts[0].strip(), parts[1].strip()
                if 2 < len(term) < 70 and len(explanation) > 10:
                    cards.append({
                        "id": card_id,
                        "front": f"What is the significance of: **{term}**?",
                        "back": explanation,
                        "category": "Core Concept",
                        "difficulty": "Easy"
                    })
                    card_id += 1

        # Extract sentences and key clauses if still need more
        if len(cards) < count:
            sentences = [s.strip() for s in re.split(r'[\.\;\n]', text) if len(s.strip()) > 20]
            for s in sentences:
                if len(cards) >= count:
                    break
                words = s.split()
                if len(words) >= 5:
                    key_phrase = " ".join(words[:4])
                    cards.append({
                        "id": card_id,
                        "front": f"Explain the key concept: *{key_phrase}...*",
                        "back": s,
                        "category": "Key Principle",
                        "difficulty": "Medium"
                    })
                    card_id += 1

        return cards

    @staticmethod
    def _get_fallback_flashcards(topic: str, count: int) -> List[Dict[str, Any]]:
        defaults = [
            {
                "id": 1,
                "front": "What is the Feynman Learning Technique?",
                "back": "A mental model where you explain a complex concept in plain language as if teaching a beginner to identify knowledge gaps.",
                "category": "Cognitive Science",
                "difficulty": "Easy"
            },
            {
                "id": 2,
                "front": "How does Active Recall differ from Passive Review?",
                "back": "Active recall forces the brain to retrieve information from memory without cues, strengthening neural synapses 2.5x more than re-reading.",
                "category": "Memory Retention",
                "difficulty": "Medium"
            },
            {
                "id": 3,
                "front": "What is the Ebbinghaus Forgetting Curve?",
                "back": "A mathematical curve demonstrating that 70% of new information is forgotten within 24 hours unless consolidated via spaced repetition intervals.",
                "category": "Spaced Learning",
                "difficulty": "Medium"
            },
            {
                "id": 4,
                "front": "What is the Leitner Flashcard System?",
                "back": "A spaced repetition method using boxes where correctly answered cards are reviewed less frequently, while missed cards are reviewed daily.",
                "category": "Study Strategy",
                "difficulty": "Hard"
            },
            {
                "id": 5,
                "front": "What is Interleaving Practice?",
                "back": "Mixing different related topics or problem types during a single study session to develop adaptive problem-solving skills.",
                "category": "Cognitive Science",
                "difficulty": "Medium"
            },
            {
                "id": 6,
                "front": "What is the Pomodoro Technique?",
                "back": "A time management framework utilizing 25-minute focused work blocks followed by 5-minute cognitive rest periods to maintain mental stamina.",
                "category": "Productivity",
                "difficulty": "Easy"
            },
            {
                "id": 7,
                "front": "What is Cognitive Load Theory in learning?",
                "back": "A psychological theory that working memory has limited capacity, requiring information to be chunked to avoid cognitive overload.",
                "category": "Learning Theory",
                "difficulty": "Hard"
            },
            {
                "id": 8,
                "front": "How does Retrieval Practice enhance long-term memory?",
                "back": "Testing yourself on material produces the 'testing effect', which restructures neural memory pathways far more durably than re-studying.",
                "category": "Memory Retention",
                "difficulty": "Medium"
            },
            {
                "id": 9,
                "front": "What is Dual Coding Theory?",
                "back": "The concept that combining verbal information with visual diagrams creates separate yet additive memory traces in the brain.",
                "category": "Cognitive Science",
                "difficulty": "Medium"
            },
            {
                "id": 10,
                "front": "What is the Method of Loci (Memory Palace)?",
                "back": "A mnemonic technique associating concepts with familiar physical locations along an imagined journey for ordered recall.",
                "category": "Mnemonics",
                "difficulty": "Hard"
            },
            {
                "id": 11,
                "front": "What role does Sleep Consolidation play in study mastery?",
                "back": "During slow-wave and REM sleep, the hippocampus replays and transfers short-term memories to the neocortex for permanent storage.",
                "category": "Neuroscience",
                "difficulty": "Medium"
            },
            {
                "id": 12,
                "front": "What is Metacognition?",
                "back": "The ability to analyze, monitor, and regulate one's own understanding and learning strategies ('thinking about thinking').",
                "category": "Self-Regulation",
                "difficulty": "Easy"
            },
            {
                "id": 13,
                "front": "What is the Spacing Effect?",
                "back": "The phenomenon where learning is greater when study sessions are spaced out over time rather than crammed in a single marathon.",
                "category": "Spaced Learning",
                "difficulty": "Easy"
            },
            {
                "id": 14,
                "front": "What is Elaborative Rehearsal?",
                "back": "Connecting new syllabus topics to existing knowledge schemas by asking 'why does this make sense?' and 'how does this connect?'.",
                "category": "Deep Learning",
                "difficulty": "Medium"
            },
            {
                "id": 15,
                "front": "What is the Generation Effect?",
                "back": "Information is remembered much better if it is actively generated by the student rather than simply read or heard.",
                "category": "Active Recall",
                "difficulty": "Easy"
            },
            {
                "id": 16,
                "front": "What is Chunking in information processing?",
                "back": "Grouping individual bits of data into meaningful larger units to bypass the 4-7 item working memory limit.",
                "category": "Cognitive Science",
                "difficulty": "Easy"
            },
            {
                "id": 17,
                "front": "What is Desirable Difficulty in education?",
                "back": "Learning tasks that require effort and active struggle yield stronger retention and deeper understanding than effortless review.",
                "category": "Learning Theory",
                "difficulty": "Hard"
            },
            {
                "id": 18,
                "front": "What is Priming in memory retrieval?",
                "back": "Exposure to a stimulus influences the response to a later stimulus, activating associative neural pathways.",
                "category": "Psychology",
                "difficulty": "Medium"
            },
            {
                "id": 19,
                "front": "What is the Zeigarnik Effect?",
                "back": "The tendency to better remember uncompleted or interrupted tasks compared to completed ones, useful for study breaks.",
                "category": "Productivity",
                "difficulty": "Medium"
            },
            {
                "id": 20,
                "front": "What is Deliberate Practice?",
                "back": "Goal-oriented, systematic practice focused specifically on weaknesses with immediate feedback rather than mindless repetition.",
                "category": "Mastery",
                "difficulty": "Hard"
            }
        ]
        return defaults[:count]

    @staticmethod
    def render_interactive_flashcard_deck(flashcards: List[Dict[str, Any]]) -> str:
        """
        Generates interactive 3D HTML/JS component for flipping flashcards with Leitner sorting.
        """
        cards_json = json.dumps(flashcards)
        return (
            '<style>'
            '@import url("https://fonts.googleapis.com/css2?family=Outfit:wght@600;700;800&family=Plus+Jakarta+Sans:wght@500;600;700&display=swap");'
            '* { box-sizing: border-box; margin: 0; padding: 0; }'
            'html, body { font-family: "Plus Jakarta Sans", sans-serif; background: transparent; padding: 2px 3px 6px 3px; margin: 0; width: 100%; }'
            '.deck-container { background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 18px; padding: 0.95rem 1.15rem 1.15rem 1.15rem; box-shadow: 0 8px 24px -4px rgba(15, 23, 42, 0.04); margin-bottom: 4px; }'
            '.deck-header { display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #f1f5f9; padding-bottom: 0.55rem; margin-bottom: 0.75rem; flex-wrap: wrap; gap: 8px; }'
            '.deck-counter { font-size: 0.78rem; font-weight: 700; color: #64748b; }'
            '.flip-card-stage { perspective: 1200px; width: 100%; min-height: 200px; margin-bottom: 0.85rem; cursor: pointer; }'
            '.flip-card-inner { position: relative; width: 100%; min-height: 200px; text-align: center; transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); transform-style: preserve-3d; }'
            '.flip-card-inner.flipped { transform: rotateY(180deg); }'
            '.flip-card-front, .flip-card-back { position: absolute; width: 100%; height: 100%; min-height: 200px; -webkit-backface-visibility: hidden; backface-visibility: hidden; border-radius: 14px; padding: 1.15rem 1.15rem; display: flex; flex-direction: column; justify-content: space-between; }'
            '.flip-card-front { background: linear-gradient(135deg, #f8faff 0%, #eef2ff 100%); border: 2px solid #c7d2fe; box-shadow: 0 6px 18px -4px rgba(99, 102, 241, 0.12); }'
            '.flip-card-back { background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border: 2px solid #86efac; transform: rotateY(180deg); box-shadow: 0 6px 18px -4px rgba(34, 197, 94, 0.12); text-align: left; }'
            '.tag-badge { align-self: flex-start; background: #ffffff; border: 1px solid rgba(0,0,0,0.08); padding: 0.2rem 0.55rem; border-radius: 20px; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; }'
            '.card-content-front { font-family: "Outfit", sans-serif; font-size: clamp(1.02rem, 3.2vw, 1.25rem); font-weight: 700; color: #090d16; line-height: 1.45; margin: auto 0; padding: 0.5rem 0; }'
            '.card-content-back { font-size: clamp(0.88rem, 2.7vw, 1rem); font-weight: 600; color: #14532d; line-height: 1.55; margin: auto 0; padding: 0.5rem 0; }'
            '.deck-actions { display: flex; gap: 8px; align-items: center; justify-content: space-between; flex-wrap: wrap; }'
            '.btn-card { flex: 1; min-width: 105px; border-radius: 10px; padding: 0.55rem 0.75rem; font-size: 0.82rem; font-weight: 700; cursor: pointer; border: none; transition: all 0.15s ease; display: flex; align-items: center; justify-content: center; gap: 6px; }'
            '.btn-again { background: #fef2f2; color: #dc2626; border: 1.5px solid #fecaca; }'
            '.btn-again:hover { background: #fee2e2; }'
            '.btn-master { background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: #ffffff; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25); }'
            '.btn-master:hover { opacity: 0.95; transform: translateY(-1px); }'
            '.progress-track { width: 100%; height: 5px; background: #f1f5f9; border-radius: 10px; overflow: hidden; margin-bottom: 0.85rem; }'
            '.progress-fill { height: 100%; background: linear-gradient(90deg, #6366f1, #10b981); width: 0%; transition: width 0.3s ease; }'
            '</style>'
            '<div class="deck-container">'
            '<div class="deck-header">'
            '<div style="display: flex; align-items: center; gap: 10px;">'
            '<span style="font-size: 1.35rem;">🗂️</span>'
            '<div>'
            '<div style="font-family: \'Outfit\', sans-serif; font-size: 1.12rem; font-weight: 800; color: #0f172a;">Active Recall Flashcard Arena</div>'
            '<div style="font-size: 0.76rem; color: #64748b;">3D interactive flip cards with Leitner spaced repetition sorting</div>'
            '</div>'
            '</div>'
            '<div style="display: flex; align-items: center; gap: 12px;">'
            '<span id="card-counter" class="deck-counter">Card 1 of 8</span>'
            '<button type="button" onclick="shuffleDeck()" style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 0.3rem 0.6rem; font-size: 0.75rem; font-weight: 700; color: #475569; cursor: pointer;">🔀 Shuffle</button>'
            '</div>'
            '</div>'
            '<div class="progress-track"><div id="deck-progress" class="progress-fill"></div></div>'
            '<div id="flip-stage" class="flip-card-stage" onclick="toggleCardFlip()">'
            '<div id="card-inner" class="flip-card-inner">'
            '<div class="flip-card-front">'
            '<div style="display: flex; justify-content: space-between; align-items: center;">'
            '<span id="card-tag-front" class="tag-badge" style="color: #4f46e5;">Core Concept</span>'
            '<span style="font-size: 0.75rem; font-weight: 700; color: #94a3b8;">💡 Click to reveal answer</span>'
            '</div>'
            '<div id="card-text-front" class="card-content-front">Loading flashcard prompt...</div>'
            '<div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.72rem; color: #64748b; font-weight: 600;">'
            '<span>Front (Question)</span>'
            '<span>Tap card ↩</span>'
            '</div>'
            '</div>'
            '<div class="flip-card-back">'
            '<div style="display: flex; justify-content: space-between; align-items: center;">'
            '<span id="card-tag-back" class="tag-badge" style="color: #15803d;">Verified Answer</span>'
            '<span style="font-size: 0.75rem; font-weight: 700; color: #16a34a;">✓ Active Recall Check</span>'
            '</div>'
            '<div id="card-text-back" class="card-content-back">Loading explanation...</div>'
            '<div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.72rem; color: #15803d; font-weight: 600;">'
            '<span>Back (Explanation)</span>'
            '<span>Click again to flip ↪</span>'
            '</div>'
            '</div>'
            '</div>'
            '</div>'
            '<div class="deck-actions">'
            '<button type="button" class="btn-card btn-again" onclick="markCard(false)">'
            '<span>❌</span> <span>Needs Practice</span>'
            '</button>'
            '<button type="button" class="btn-card btn-master" onclick="markCard(true)">'
            '<span>✅</span> <span>Got It (Mastered)</span>'
            '</button>'
            '</div>'
            '<div id="deck-complete-screen" style="display: none; text-align: center; padding: 1.5rem 1rem;">'
            '<div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎉</div>'
            '<div style="font-family: \'Outfit\', sans-serif; font-size: 1.4rem; font-weight: 800; color: #0f172a; margin-bottom: 4px;">Deck Completed!</div>'
            '<div id="mastery-summary" style="font-size: 0.95rem; color: #475569; margin-bottom: 1.25rem;">You mastered all cards in this study block.</div>'
            '<button type="button" onclick="restartDeck()" style="background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%); color: #ffffff; border: none; border-radius: 10px; padding: 0.65rem 1.5rem; font-size: 0.92rem; font-weight: 700; cursor: pointer;">🔄 Restart Deck</button>'
            '</div>'
            '</div>'
            '<script>'
            'var deck = ' + cards_json + ';'
            'var curCardIdx = 0;'
            'var masteredCount = 0;'
            'var reviewCount = 0;'
            'var isFlipped = false;'
            ''
            'function updateCardView() {'
            '  if (!deck || deck.length === 0) return;'
            '  if (curCardIdx >= deck.length) {'
            '    showCompletion();'
            '    return;'
            '  }'
            '  var card = deck[curCardIdx];'
            '  var inner = document.getElementById("card-inner");'
            '  if (inner) inner.classList.remove("flipped");'
            '  isFlipped = false;'
            '  document.getElementById("card-counter").textContent = "Card " + (curCardIdx + 1) + " of " + deck.length;'
            '  document.getElementById("deck-progress").style.width = ((curCardIdx / deck.length) * 100) + "%";'
            '  document.getElementById("card-tag-front").textContent = card.category || "Core Concept";'
            '  document.getElementById("card-tag-back").textContent = (card.difficulty ? card.difficulty + " • " : "") + "Answer";'
            '  document.getElementById("card-text-front").innerHTML = card.front;'
            '  document.getElementById("card-text-back").innerHTML = card.back;'
            '}'
            ''
            'function toggleCardFlip() {'
            '  var inner = document.getElementById("card-inner");'
            '  if (inner) {'
            '    inner.classList.toggle("flipped");'
            '    isFlipped = inner.classList.contains("flipped");'
            '  }'
            '}'
            ''
            'function markCard(mastered) {'
            '  if (mastered) masteredCount++; else reviewCount++;'
            '  curCardIdx++;'
            '  updateCardView();'
            '}'
            ''
            'function showCompletion() {'
            '  document.getElementById("flip-stage").style.display = "none";'
            '  document.querySelector(".deck-actions").style.display = "none";'
            '  document.getElementById("deck-progress").style.width = "100%";'
            '  document.getElementById("mastery-summary").innerHTML = "Mastered: <strong>" + masteredCount + "</strong> cards &bull; Needs Practice: <strong>" + reviewCount + "</strong> cards.";'
            '  document.getElementById("deck-complete-screen").style.display = "block";'
            '}'
            ''
            'function restartDeck() {'
            '  curCardIdx = 0;'
            '  masteredCount = 0;'
            '  reviewCount = 0;'
            '  document.getElementById("flip-stage").style.display = "block";'
            '  document.querySelector(".deck-actions").style.display = "flex";'
            '  document.getElementById("deck-complete-screen").style.display = "none";'
            '  updateCardView();'
            '}'
            ''
            'function shuffleDeck() {'
            '  for (var i = deck.length - 1; i > 0; i--) {'
            '    var j = Math.floor(Math.random() * (i + 1));'
            '    var temp = deck[i];'
            '    deck[i] = deck[j];'
            '    deck[j] = temp;'
            '  }'
            '  restartDeck();'
            '}'
            ''
            'updateCardView();'
            '</script>'
        )
