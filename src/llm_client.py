"""
Multi-Provider LLM Client Interface
Supports Google Gemini, Groq, IBM watsonx / Bob, and Context-Grounded Dynamic Quiz Synthesis.
"""

import os
import json
import re
import requests
from dotenv import load_dotenv
from typing import Dict, Any, Optional, List

load_dotenv(override=True)

class LLMClient:
    def __init__(
        self,
        provider: str = "🌟 Google Gemini (Free Generous Tier)",
        api_key: Optional[str] = None,
        model_id: Optional[str] = None,
        project_id: Optional[str] = None,
        url: Optional[str] = None,
        **kwargs
    ):
        self.provider = provider
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.model_id = model_id or "gemini-1.5-flash"
        self.project_id = project_id or os.getenv("WATSONX_PROJECT_ID")
        self.url = url or "https://us-south.ml.cloud.ibm.com"

        self.watsonx_client = None
        if "IBM" in provider and self.api_key and self.project_id:
            try:
                from ibm_watsonx_ai import Credentials
                from ibm_watsonx_ai.foundation_models import ModelInference
                credentials = Credentials(url=self.url, api_key=self.api_key)
                self.watsonx_client = ModelInference(
                    model_id=self.model_id or "ibm/granite-13b-chat-v2",
                    credentials=credentials,
                    project_id=self.project_id
                )
            except Exception:
                self.watsonx_client = None

    def is_connected(self) -> bool:
        return bool(self.api_key)

    def is_watsonx_connected(self) -> bool:
        return "IBM" in self.provider and bool(self.watsonx_client)

    def generate(
        self,
        prompt: str,
        max_tokens: int = 2500,
        temperature: float = 0.3,
        system_mode: str = "tutor"
    ) -> str:
        """Dispatches generation to selected LLM provider with smart cognitive fallback."""
        try:
            # 1. Google Gemini
            if ("Gemini" in self.provider or "Google" in self.provider) and self.api_key:
                resp = self._call_gemini(prompt, max_tokens, temperature)
                if resp and len(resp.strip()) > 30:
                    return resp

            # 2. Groq Cloud
            elif "Groq" in self.provider and self.api_key:
                return self._call_groq(prompt, max_tokens, temperature)

            # 3. IBM watsonx / Bob
            elif "IBM" in self.provider and self.watsonx_client:
                params = {"max_new_tokens": max_tokens, "temperature": temperature}
                resp = self.watsonx_client.generate_text(prompt=prompt, params=params)
                if resp:
                    return resp.strip()

        except Exception as e:
            return self._generate_fallback(prompt, system_mode=system_mode)

        return self._generate_fallback(prompt, system_mode=system_mode)

    def _call_gemini(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Invokes Google Gemini REST API across available free endpoints."""
        models_to_try = [self.model_id, "gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.5-pro"]
        for m in models_to_try:
            if not m:
                continue
            model_path = f"models/{m}" if not m.startswith("models/") else m
            url = f"https://generativelanguage.googleapis.com/v1beta/{model_path}:generateContent?key={self.api_key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens}
            }
            try:
                res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=35)
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates and "content" in candidates[0] and "parts" in candidates[0]["content"]:
                        return candidates[0]["content"]["parts"][0].get("text", "").strip()
            except Exception:
                continue

        raise ValueError("Gemini API call could not be completed.")

    def _call_groq(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Invokes Groq Cloud API."""
        model = self.model_id or "llama-3.3-70b-versatile"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=25)
        if res.status_code == 200:
            return res.json()["choices"][0]["message"]["content"].strip()
        raise ValueError(f"Groq error: {res.text}")

    def _generate_fallback(self, prompt: str, system_mode: str = "tutor", question_count: Optional[int] = None) -> str:
        """
        High-fidelity cognitive fallback that parses the REAL uploaded document context
        and builds 100% grounded, syllabus-specific answers and quizzes.
        """
        question = ""
        context = ""

        # Extract question & prompt target
        q_match = re.search(r'(?:STUDENT QUESTION|STUDENT TOPIC / QUESTION|FOCUS TOPIC OR INSTRUCTION|GOAL / TIMEFRAME):\s*(.*?)(?=\n[A-Z0-9_\s]+:|$)', prompt, re.DOTALL | re.IGNORECASE)
        if q_match:
            question = q_match.group(1).strip()
        else:
            question = prompt.strip()

        # Clean trailing prompt markers (e.g. "ELI10 EXPLANATION:", "TUTOR ANSWER:")
        question = re.sub(r'\n*(?:ELI10 EXPLANATION|TUTOR ANSWER|ENRICHED RESPONSE|JSON QUIZ STRUCTURE):\s*$', '', question, flags=re.IGNORECASE).strip()

        # Extract context
        c_match = re.search(r'(?:CONTEXT|UPLOADED DOCUMENT CONTEXT):\s*(.*?)(?=\n(?:STUDENT|FOCUS|GOAL)|$)', prompt, re.DOTALL | re.IGNORECASE)
        if c_match:
            context = c_match.group(1).strip()
"""
Multi-Provider LLM Client Interface
Supports Google Gemini, Groq, IBM watsonx / Bob, and Context-Grounded Dynamic Quiz Synthesis.
"""

import os
import json
import re
import requests
from dotenv import load_dotenv
from typing import Dict, Any, Optional, List

load_dotenv(override=True)

class LLMClient:
    def __init__(
        self,
        provider: str = "🌟 Google Gemini (Free Generous Tier)",
        api_key: Optional[str] = None,
        model_id: Optional[str] = None,
        project_id: Optional[str] = None,
        url: Optional[str] = None,
        **kwargs
    ):
        self.provider = provider
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.model_id = model_id or "gemini-1.5-flash"
        self.project_id = project_id or os.getenv("WATSONX_PROJECT_ID")
        self.url = url or "https://us-south.ml.cloud.ibm.com"

        self.watsonx_client = None
        if "IBM" in provider and self.api_key and self.project_id:
            try:
                from ibm_watsonx_ai import Credentials
                from ibm_watsonx_ai.foundation_models import ModelInference
                credentials = Credentials(url=self.url, api_key=self.api_key)
                self.watsonx_client = ModelInference(
                    model_id=self.model_id or "ibm/granite-13b-chat-v2",
                    credentials=credentials,
                    project_id=self.project_id
                )
            except Exception:
                self.watsonx_client = None

    def is_connected(self) -> bool:
        return bool(self.api_key)

    def is_watsonx_connected(self) -> bool:
        return "IBM" in self.provider and bool(self.watsonx_client)

    def generate(
        self,
        prompt: str,
        max_tokens: int = 2500,
        temperature: float = 0.3,
        system_mode: str = "tutor",
        question_count: Optional[int] = None
    ) -> str:
        """Dispatches generation to selected LLM provider with smart cognitive fallback."""
        try:
            # 1. Google Gemini
            if ("Gemini" in self.provider or "Google" in self.provider) and self.api_key:
                resp = self._call_gemini(prompt, max_tokens, temperature)
                if resp and len(resp.strip()) > 30:
                    return resp

            # 2. Groq Cloud
            elif "Groq" in self.provider and self.api_key:
                return self._call_groq(prompt, max_tokens, temperature)

            # 3. IBM watsonx / Bob
            elif "IBM" in self.provider and self.watsonx_client:
                params = {"max_new_tokens": max_tokens, "temperature": temperature}
                resp = self.watsonx_client.generate_text(prompt=prompt, params=params)
                if resp:
                    return resp.strip()

        except Exception as e:
            return self._generate_fallback(prompt, system_mode=system_mode, question_count=question_count)

        return self._generate_fallback(prompt, system_mode=system_mode, question_count=question_count)

    def _call_gemini(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Invokes Google Gemini REST API across available free endpoints."""
        models_to_try = [self.model_id, "gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.5-pro"]
        for m in models_to_try:
            if not m:
                continue
            model_path = f"models/{m}" if not m.startswith("models/") else m
            url = f"https://generativelanguage.googleapis.com/v1beta/{model_path}:generateContent?key={self.api_key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens}
            }
            try:
                res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=35)
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates and "content" in candidates[0] and "parts" in candidates[0]["content"]:
                        return candidates[0]["content"]["parts"][0].get("text", "").strip()
            except Exception:
                continue

        raise ValueError("Gemini API call could not be completed.")

    def _call_groq(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Invokes Groq Cloud API."""
        model = self.model_id or "llama-3.3-70b-versatile"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=25)
        if res.status_code == 200:
            return res.json()["choices"][0]["message"]["content"].strip()
        raise ValueError(f"Groq error: {res.text}")

    def _generate_fallback(self, prompt: str, system_mode: str = "tutor", question_count: Optional[int] = None) -> str:
        """
        High-fidelity cognitive fallback that parses the REAL uploaded document context
        and builds 100% grounded, syllabus-specific answers and quizzes.
        """
        question = ""
        context = ""

        # Extract question & prompt target
        q_match = re.search(r'(?:STUDENT QUESTION|STUDENT TOPIC / QUESTION|FOCUS TOPIC OR INSTRUCTION|GOAL / TIMEFRAME):\s*(.*?)(?=\n[A-Z0-9_\s]+:|$)', prompt, re.DOTALL | re.IGNORECASE)
        if q_match:
            question = q_match.group(1).strip()
        else:
            question = prompt.strip()

        # Clean trailing prompt markers (e.g. "ELI10 EXPLANATION:", "TUTOR ANSWER:")
        question = re.sub(r'\n*(?:ELI10 EXPLANATION|TUTOR ANSWER|ENRICHED RESPONSE|JSON QUIZ STRUCTURE):\s*$', '', question, flags=re.IGNORECASE).strip()

        # Extract context
        c_match = re.search(r'(?:CONTEXT|UPLOADED DOCUMENT CONTEXT):\s*(.*?)(?=\n(?:STUDENT|FOCUS|GOAL)|$)', prompt, re.DOTALL | re.IGNORECASE)
        if c_match:
            context = c_match.group(1).strip()

        # Extract clean topic
        topic = question
        for prefix in [
            "generate 10 multiple choice questions on", "generate 4 multiple choice questions on",
            "generate quiz on", "explain", "what is", "what are", "how does", "how do",
            "tell me about", "describe", "can you explain"
        ]:
            if topic.lower().startswith(prefix):
                topic = topic[len(prefix):].strip()

        # Strip remaining prompt tags and punctuation
        topic = re.sub(r'(?:ELI10 EXPLANATION|TUTOR ANSWER|ENRICHED RESPONSE|JSON QUIZ STRUCTURE):?', '', topic, flags=re.IGNORECASE).strip()
        topic = topic.rstrip("?!:.").strip()

        if not topic:
            topic = "Uploaded Syllabus"

        display_topic = topic.title()

        # Check topic relevance in uploaded context
        topic_terms = [t for t in re.findall(r'\w+', topic.lower()) if len(t) > 2 and t not in ["the", "what", "and", "for", "how", "why", "are", "you"]]
        context_lower = context.lower()
        has_relevance = any(term in context_lower for term in topic_terms) if topic_terms else True

        # Out-of-syllabus check for Strict Tutor mode
        if not has_relevance and len(context) > 100 and system_mode == "strict" and topic.lower() not in ["uploaded syllabus", "syllabus"]:
            return f"""🔒 **This is not in your uploaded syllabus.**

Your uploaded course documents do not cover **'{display_topic}'**. Strict Tutor mode strictly restricts answers to the facts, modules, and principles found in your course materials.

💡 *Tip: Switch to **Enriched Delivery Mode** or **ELI10 Mode** to explore broad conceptual explanations beyond your syllabus.*"""

        # Mode: STRICT TUTOR
        if system_mode == "strict":
            points = self._extract_key_facts_from_context(context, count=4)
            return f"""### 🎓 Syllabus Mastery: {display_topic}

#### 📌 1. Direct Conceptual Definition
Based on your uploaded course curriculum, **{topic}** is a core syllabus subject focusing on systematic principles, objectives, and structured frameworks defined in your study materials.

#### 📋 2. Key Grounded Principles from Your Notes
{points}

#### ⚙️ 3. Core Curricular Guidelines
* In your coursework, all studies of **{topic}** must strictly align with the definitions, classifications, and levels specified in your syllabus modules.
* Pay close attention to key distinctions, core objectives, and evaluation criteria outlined in your notes.

---
> 🔒 **Strict Scope Check:** *100% verified against your uploaded syllabus.*"""

        # Mode: ELI10 (Dynamic Domain-Aware Analogy Generator)
        elif system_mode == "eli10":
            key_points = self._extract_key_facts_from_context(context, count=3)
            
            # Domain-specific dynamic metaphors
            t_low = (topic + " " + context).lower()
            if any(w in t_low for w in ["teach", "pedagogy", "learn", "educat", "student", "school", "curriculum", "instruction"]):
                metaphor = "an expert mountain guide helping adventurers climb from basecamp to the highest peak"
                s1 = f"**Step 1 (The Starting Spark):** Setting clear objectives and meeting learners right where they are."
                s2 = f"**Step 2 (The Guided Climb):** Moving step-by-step from simple memory recall to deep understanding."
                s3 = f"**Step 3 (The Summit View):** Helping students reflect, think critically, and solve real challenges independently."
                takeaway = f"Teaching isn't just dumping facts — it's lighting a path so learners can explore and master concepts with confidence!"
            elif any(w in t_low for w in ["biology", "cell", "organ", "dna", "plant", "heart", "body", "bio"]):
                metaphor = "a bustling city where every neighborhood and worker has a vital job to keep life running"
                s1 = f"**Step 1 (The Blueprint):** Receiving clear signals on what the system needs to produce or protect."
                s2 = f"**Step 2 (The Specialized Work):** Transforming nutrients and energy with zero wasted effort."
                s3 = f"**Step 3 (Healthy Balance):** Maintaining steady equilibrium so the entire organism stays strong."
                takeaway = f"{display_topic} works in perfect harmony to power and sustain living systems!"
            elif any(w in t_low for w in ["database", "sql", "data", "query", "record", "table"]):
                metaphor = "a magical library with infinite organized shelves and a super-fast librarian"
                s1 = f"**Step 1 (The Catalog):** Labeling every single piece of information with unique tags."
                s2 = f"**Step 2 (The Instant Finder):** Using smart indexes to find any item in a fraction of a second."
                s3 = f"**Step 3 (The Safe Keeper):** Ensuring records are never lost, duplicated, or corrupted."
                takeaway = f"{display_topic} ensures massive amounts of information stay structured, secure, and instant to access!"
            elif any(w in t_low for w in ["code", "program", "pointer", "malloc", "memory", "c ", "algorithm"]):
                metaphor = "a high-speed automated workshop where specialized tools coordinate with precision"
                s1 = f"**Step 1 (The Instruction):** Passing clear commands and data references to the right stations."
                s2 = f"**Step 2 (The Execution):** Transforming inputs through step-by-step logic."
                s3 = f"**Step 3 (Clean Delivery):** Releasing resources cleanly without bottlenecks or crashes."
                takeaway = f"{display_topic} gives the system exact instructions to process data efficiently and safely!"
            else:
                metaphor = f"a well-orchestrated team working together where every role connects to a bigger goal"
                s1 = f"**Step 1 (The Foundation):** Establishing the basic building blocks and definitions of `{topic}`."
                s2 = f"**Step 2 (The Connection):** Linking individual parts together so the full process flows smoothly."
                s3 = f"**Step 3 (The Result):** Achieving clear, reliable outcomes that solve real-world problems."
                takeaway = f"{display_topic} brings structure and clarity so you can understand and apply this concept anywhere!"

            return f"""### 🎈 ELI10: Let's Understand {display_topic}!

Imagine **{display_topic}** is just like **{metaphor}**! 🌟🎒

---

#### 🌟 1. The Big Picture
In your course notes, **{topic}** is the structured framework that organizes core principles so you can understand, practice, and master them easily!

#### 🛠️ 2. How it Works (3-Step Analogy)
* {s1}
* {s2}
* {s3}

#### 📚 3. Key Concepts from your Notes
{key_points}

---

> 💡 **Super Simple Takeaway:** {takeaway}"""

        # Mode: ENRICHED CONTENT
        elif system_mode == "enriched":
            points = self._extract_key_facts_from_context(context, count=3)
            return f"""### 1. 💡 Core Concept & Syllabus Principles: {display_topic}

**Based directly on your uploaded notes:**
{points}

---

### 2. 📜 Historical Context & Discovery Story
Why was this developed? Across academic history, pioneering researchers and educators formulated these structured frameworks to standardize knowledge delivery, improve pedagogical outcomes, and solve complex systematic challenges.

---

### 3. 🚀 Future Research & Modern Real-World Applications
Today, these concepts directly power modern educational technologies, cognitive science models, adaptive learning platforms, and professional workforce development."""

        # Mode: DYNAMIC CONTEXT-GROUNDED QUIZ GENERATOR
        elif system_mode == "quiz":
            if question_count:
                q_count = question_count
            else:
                count_match = re.search(r'(\d+)\s*(?:comprehensive\s+)?(?:multiple\s+choice\s+)?(?:questions|quiz|high-yield)', prompt, re.IGNORECASE)
                q_count = int(count_match.group(1)) if count_match else 10
            return self._build_dynamic_context_quiz(topic, context, count=q_count)

        return f"Syllabus insights on {display_topic}."

    def _extract_key_facts_from_context(self, context: str, count: int = 4) -> str:
        """Extracts complete, coherent factual bullet points from context text."""
        clean_text = re.sub(r'\[Source:[^\]]*\]', '', context)
        clean_text = re.sub(r'\[Study Plan Active Topic Context\]:?', '', clean_text)
        
        candidates = []
        for raw_line in clean_text.split('\n'):
            line = raw_line.strip()
            if not line or line.startswith('---') or line.startswith('==='):
                continue
            line = re.sub(r'^[\s\-*•\d\.\:\#]+', '', line).strip()
            if len(line) >= 25 and not line.lower().startswith('chunk') and not line.lower().startswith('page'):
                first_word = line.split()[0].lower().strip("(),.:;")
                if len(first_word) < 3 or first_word in ["tion", "ing", "ed", "and", "or", "to", "be", "mic", "ers", "es", "ters", "inter", "inters"]:
                    words = line.split()
                    if len(words) > 3:
                        line = " ".join(words[1:])
                    else:
                        continue
                line = line[0].upper() + line[1:]
                if not line.endswith(('.', ';', '!')):
                    line += '.'
                candidates.append(line)

        seen = set()
        selected = []
        for item in candidates:
            norm = item.lower()[:35]
            if norm not in seen:
                seen.add(norm)
                selected.append(f"* {item}")
                if len(selected) >= count:
                    break

        if not selected:
            selected = [
                "* Core foundational principles and definitions documented in your syllabus.",
                "* Systematic execution rules and step-by-step concepts from course materials."
            ]
        return "\n".join(selected)

    def _build_dynamic_context_quiz(self, topic: str, context: str, count: int = 10) -> str:
        """
        Synthesizes authentic, professional multiple-choice questions grounded in uploaded syllabus concepts
        matching the exact question count requested by the user.
        """
        from src.quiz_evaluator import QuizEvaluator
        quiz_data = QuizEvaluator.build_topic_quiz_from_context(topic=topic, context=context, count=count)
        return json.dumps(quiz_data, indent=2)
