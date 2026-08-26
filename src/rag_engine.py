"""
RAG Engine Orchestrator
Binds Document Ingestion, ChromaDB Retrieval, Prompt Engineering, and LLM Inference.
"""

import time
from typing import Dict, Any, List, Optional
from src.ingestion import DocumentIngestionPipeline
from src.llm_client import LLMClient
from src.prompts import (
    STRICT_TUTOR_SYSTEM_PROMPT,
    ELI10_SYSTEM_PROMPT,
    ENRICHED_CONTENT_SYSTEM_PROMPT,
    QUIZ_GENERATOR_SYSTEM_PROMPT,
    STUDY_PLAN_SYSTEM_PROMPT
)
from src.quiz_evaluator import QuizEvaluator

class RAGEngine:
    def __init__(
        self,
        ingestion_pipeline: DocumentIngestionPipeline,
        llm_client: LLMClient
    ):
        self.ingestion = ingestion_pipeline
        self.llm = llm_client

    def answer_query(
        self,
        query: str,
        mode: str = "strict",  # "strict", "eli10", "enriched", "quiz", "plan"
        top_k: int = 4,
        topic_context_override: Optional[str] = None,
        question_count: int = 10
    ) -> Dict[str, Any]:
        """
        Executes end-to-end RAG query:
        1. Retrieves relevant syllabus chunks from ChromaDB.
        2. Combines with optional Study Plan topic context.
        3. Selects prompt template based on learning mode.
        4. Invokes LLM (IBM watsonx / Bob / cognitive fallback).
        5. Returns answer, source citations, and parsed quiz data if applicable.
        """
        start_time = time.time()

        # Step 1: Retrieve context chunks
        all_chunks = self.ingestion.get_all_chunks(limit=30)
        
        # If quiz mode or small document, pass comprehensive chunks
        if mode in ["quiz", "plan"] or len(all_chunks) <= 6:
            chunks = all_chunks
        else:
            chunks = self.ingestion.query_similarity(query_text=query, n_results=top_k)
            if not chunks:
                chunks = all_chunks[:top_k]

        if not chunks and not topic_context_override:
            context_text = "NO COURSE MATERIALS UPLOADED. (Please upload your syllabus or lecture notes first)."
        else:
            context_parts = []
            if topic_context_override:
                context_parts.append(f"[Study Plan Active Topic Context]:\n{topic_context_override}")
            for idx, c in enumerate(chunks):
                source = c["metadata"].get("source", "Uploaded Document")
                part = f"[Source: {source} | Chunk {idx+1}]\n{c['content']}"
                context_parts.append(part)
            context_text = "\n\n".join(context_parts)

        # Step 2: Select Prompt Template
        if mode == "strict":
            prompt = STRICT_TUTOR_SYSTEM_PROMPT.format(context=context_text, question=query)
        elif mode == "eli10":
            prompt = ELI10_SYSTEM_PROMPT.format(context=context_text, question=query)
        elif mode == "enriched":
            prompt = ENRICHED_CONTENT_SYSTEM_PROMPT.format(context=context_text, question=query)
        elif mode == "quiz":
            prompt = QUIZ_GENERATOR_SYSTEM_PROMPT.format(context=context_text, question=query)
        elif mode == "plan":
            prompt = STUDY_PLAN_SYSTEM_PROMPT.format(context=context_text, question=query)
        else:
            prompt = STRICT_TUTOR_SYSTEM_PROMPT.format(context=context_text, question=query)

        # Step 3: LLM Inference
        raw_response = self.llm.generate(
            prompt=prompt,
            system_mode=mode
        )

        latency = round(time.time() - start_time, 2)

        # Step 4: Parse quiz if in quiz mode
        quiz_data = None
        if mode == "quiz":
            quiz_data = QuizEvaluator.parse_quiz_json(raw_response)
            if not quiz_data:
                # Clean topic name from query
                clean_topic = re.sub(
                    r'^(?:generate|create|make)\s+(?:at least\s+)?(?:\d+\s+)?(?:multiple choice\s+)?(?:questions|quiz)\s+(?:on|about|for)?\s*',
                    '',
                    query,
                    flags=re.IGNORECASE
                )
                clean_topic = clean_topic.replace("strictly based on the uploaded document context", "").strip()
                quiz_data = QuizEvaluator.build_topic_quiz_from_context(
                    topic=clean_topic,
                    context=context_text,
                    count=question_count
                )

        return {
            "query": query,
            "mode": mode,
            "answer": raw_response,
            "quiz_data": quiz_data,
            "context_chunks": chunks,
            "chunk_count": len(chunks),
            "latency_seconds": latency,
            "is_watsonx": self.llm.is_connected()
        }
