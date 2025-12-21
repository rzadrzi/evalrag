# rag/generator.py

import time
from typing import Dict, Any

from rag import Retriever, build_rag_prompt


class RAGGenerator:
    def __init__(self, retriever: Retriever, llm_client):
        self.retriever = retriever
        self.llm_client = llm_client

    def answer_question(
        self,
        question: str,
        source_id: str | None = None,
        top_k: int | None = None,
    ) -> Dict[str, Any]:
        # 1. retrieve contexts
        contexts = self.retriever.retrieve(
            question=question,
            source_id=source_id,
            top_k=top_k,
        )

        # 2. build prompt
        prompt = build_rag_prompt(
            question=question,
            contexts=contexts,
        )

        # 3. call LLM
        start = time.time()
        llm_response = self.llm_client.generate(prompt)
        latency_ms = int((time.time() - start) * 1000)

        # llm_response
        answer_text = llm_response["text"]
        usage = llm_response.get("usage", {})

        # 4. pack result
        result = {
            "answer": answer_text,
            "contexts": contexts,
            "meta": {
                "latency_ms": latency_ms,
                "model": llm_response.get("model"),
                "tokens_prompt": usage.get("prompt_tokens"),
                "tokens_completion": usage.get("completion_tokens"),
            },
        }
        return result
