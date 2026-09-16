from fastapi.testclient import TestClient

from backend.main import app
from backend.api.ask import rag_service


client = TestClient(app)


class FakeLLMService:
    def generate(self, prompt: str) -> str:
        return (
            "Supervised learning is a machine learning approach "
            "where a model learns from labeled training data. "
            "[Source: machine_learning.pdf, Page: 5]"
        )


class FakeRetrievalService:
    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:

        return [
            {
                "chunk_id": "test_chunk_1",
                "text": (
                    "Supervised learning uses labeled "
                    "training data."
                ),
                "metadata": {
                    "document_id": "test_document",
                    "filename": "machine_learning.pdf",
                    "page": 5,
                    "chunk_index": 0,
                },
                "distance": 0.2,
            }
        ]


def test_ask_endpoint():
    original_llm_service = rag_service.llm_service
    original_retrieval_service = (
        rag_service.retrieval_service
    )

    rag_service.llm_service = FakeLLMService()
    rag_service.retrieval_service = (
        FakeRetrievalService()
    )

    try:
        response = client.post(
            "/ask",
            json={
                "question": (
                    "What is supervised learning?"
                ),
                "top_k": 5,
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert "conversation_id" in data
        assert "question" in data
        assert "answer" in data
        assert "sources" in data

        assert (
            data["question"]
            == "What is supervised learning?"
        )

        assert "Supervised learning" in data["answer"]

        assert len(data["sources"]) == 1

        assert (
            data["sources"][0]["filename"]
            == "machine_learning.pdf"
        )

        assert (
            data["sources"][0]["page"]
            == 5
        )

    finally:
        rag_service.llm_service = (
            original_llm_service
        )

        rag_service.retrieval_service = (
            original_retrieval_service
        )