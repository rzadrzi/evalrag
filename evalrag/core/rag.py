# evalrag/core/rag.py

import time
from typing import List, Dict, Any
from evalrag.core.config import get_prompt_template


class RAG:
    """
    Unified RAG system for retrieval-augmented generation.

    Combines retrieval, prompt building, and LLM generation into a single
    class. Responsibilities:
      - Retrieve relevant context chunks from a vector store via `retrieve()`.
      - Build prompts via `build_rag_prompt()` combining questions and contexts.
      - Generate answers via `answer_question()` using an LLM.

    Typical workflow:
      1. Call `retrieve(question)` to fetch context chunks.
      2. Call `build_rag_prompt(question, contexts)` to create the prompt.
      3. Call `answer_question(question)` to get the full RAG response.
    """
    def __init__(self, vector_client, embedder, llm_client, top_k: int = 5):
        """
        Initialize the RagSys.

        Args:
            vector_client: A vector search client exposing a `search` method.
            embedder: An embeddings client exposing an `embed` or `embed_query` method.
            llm_client: An LLM client exposing a `generate(prompt)` method.
            top_k: Default number of results to return for retrieval.
        """
        self.vector_client = vector_client
        self.embedder = embedder
        self.top_k = top_k
        self.llm_client = llm_client

    def retrieve(
        self, question: str, source_id: str | None = None, top_k: int | None = None
    ) -> List[Dict]:
        """
        Retrieve top-k context chunks relevant to `question`.

        Args:
            question: User question text to embed and search for.
            source_id: Optional filter to restrict results to a specific source.
            top_k: Optional override for number of results to return.

        Returns:
            A list of dicts with keys `doc_id`, `chunk_id`, `text`, `score`, and `metadata`.
        """

        k = top_k or self.top_k

        query_embedding = self.embedder.embed(question)

        # This only a concept of vectorDB
        results = self.vector_client.search(
            embedding=query_embedding,
            top_k=k,
            filter={"source_id": source_id} if source_id else None,
        )

        contexts = []
        for hit in results:
            contexts.append(
                {
                    "doc_id": hit.payload["doc_id"],
                    "chunk_id": hit.payload["chunk_id"],
                    "text": hit.payload["text"],
                    "score": hit.score,
                    "metadata": hit.payload.get("metadata", {}),
                }
            )

        return contexts
    
    def build_context_block(self, contexts: List[Dict], max_chars: int = 4000) -> str:
        """
        Concatenate retrieved context chunks into a single block for the prompt.

        The function joins context texts separated by a visual delimiter and
        ensures the total character length does not exceed `max_chars`.

        Args:
            contexts: List of context dicts produced by `Retriever.retrieve`.
            max_chars: Maximum cumulative characters to include.

        Returns:
            A single string containing the joined context texts.
        """

        parts = []
        total = 0
        for c in contexts:
            txt = c["text"].strip()
            if not txt:
                continue
            if total + len(txt) > max_chars:
                break
            parts.append(txt)
            total += len(txt)
        return "\n\n---\n\n".join(parts)

    # RAG prompt building functions
    def build_rag_prompt(self, question: str, contexts: List[Dict]) -> str:
        """
        Build the full RAG prompt by injecting the question and context block
        into the prompt template.

        Args:
            question: The user question string.
            contexts: Retrieved context dictionaries to include in the prompt.

        Returns:
            A formatted prompt string ready to be sent to an LLM.
        """
        RAG_PROMPT_TEMPLATE = get_prompt_template()

        context_block = self.build_context_block(contexts)

        return RAG_PROMPT_TEMPLATE.format(
            question=question,
            context_block=context_block,
        )
    
    def generate_answer(
        self,
        question: str,
        source_id: str | None = None,
        top_k: int | None = None,
    ) -> Dict[str, Any]:
        """
        Answer a question using retrieval-augmented generation.

        Steps performed:
          1. Retrieve relevant contexts from the vector store.
          2. Build a prompt containing the question and contexts.
          3. Call the LLM to generate an answer and measure latency.
          4. Return the answer along with contexts and metadata.

        Args:
            question: The user question to answer.
            source_id: Optional filter to restrict retrieval to a specific source.
            top_k: Optional override for how many context chunks to retrieve.

        Returns:
            A dict containing `answer`, `contexts`, and `meta` information.
        """

        # 1. retrieve contexts
        contexts = self.retrieve(
            question=question,
            source_id=source_id,
            top_k=top_k,
        )

        # 2. build prompt
        prompt = self.build_rag_prompt(
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

# End of evalrag/core/rag.py