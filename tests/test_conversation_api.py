from fastapi.testclient import TestClient

from backend.main import app
from backend.api.ask import rag_service


client = TestClient(app)


class FakeLLMService:
    def generate(self, prompt: str) -> str:
        return (
            "Supervised learning uses labeled training data. "
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


def test_conversation_persistence():

    original_llm_service = rag_service.llm_service
    original_retrieval_service = (
        rag_service.retrieval_service
    )

    rag_service.llm_service = FakeLLMService()
    rag_service.retrieval_service = (
        FakeRetrievalService()
    )

    try:
        # First question
        first_response = client.post(
            "/ask",
            json={
                "question": (
                    "What is supervised learning?"
                ),
                "top_k": 5,
            },
        )

        assert first_response.status_code == 200

        first_data = first_response.json()

        conversation_id = (
            first_data["conversation_id"]
        )

        assert conversation_id is not None

        # Second question in same conversation

        second_response = client.post(
            "/ask",
            json={
                "question": (
                    "What type of data does it use?"
                ),
                "top_k": 5,
                "conversation_id": conversation_id,
            },
        )

        assert second_response.status_code == 200

        second_data = second_response.json()

        assert (
            second_data["conversation_id"]
            == conversation_id
        )

        # Retrieve stored messages
        messages_response = client.get(
            f"/conversations/"
            f"{conversation_id}/messages"
        )

        assert messages_response.status_code == 200

        messages_data = (
            messages_response.json()
        )

        messages = messages_data["messages"]

        # Two questions + two answers
        assert len(messages) == 4

        # First user message
        assert messages[0]["role"] == "user"

        assert (
            messages[0]["content"]
            == "What is supervised learning?"
        )

        # First assistant message
        assert (
            messages[1]["role"]
            == "assistant"
        )

        # Second user message
        assert messages[2]["role"] == "user"

        assert (
            messages[2]["content"]
            == "What type of data does it use?"
        )

        # Second assistant message
        assert (
            messages[3]["role"]
            == "assistant"
        )

    finally:

        rag_service.llm_service = (
            original_llm_service
        )

        rag_service.retrieval_service = (
            original_retrieval_service
        )