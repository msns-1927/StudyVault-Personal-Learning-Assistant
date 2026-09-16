from backend.services.embedding_service import EmbeddingService
from backend.services.vector_store import VectorStore


class RetrievalService:
    def __init__(
        self,
        embedding_service: EmbeddingService | None = None,
        vector_store: VectorStore | None = None,
    ):
        self.embedding_service = (
            embedding_service
            if embedding_service is not None
            else EmbeddingService()
        )

        self.vector_store = (
            vector_store
            if vector_store is not None
            else VectorStore()
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:
        """
        Retrieve the most relevant chunks for a user query.
        """

        if not query.strip():
            raise ValueError("Query cannot be empty.")

        query_embedding = (
            self.embedding_service.generate_embedding(query)
        )

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        return results