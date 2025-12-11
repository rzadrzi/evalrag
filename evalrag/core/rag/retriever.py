# rag/retriever.py

from typing import List, Dict


class Retriever:
    def __init__(self, vector_client, embedder, top_k: int = 5):
        self.vector_client = vector_client
        self.embedder = embedder
        self.top_k = top_k

    def retrieve(
        self, question: str, source_id: str | None = None, top_k: int | None = None
    ) -> List[Dict]:
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
