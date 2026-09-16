from backend.services.retrieval_service import RetrievalService


class FakeEmbeddingService:
    def generate_embedding(self, text: str):
        return [0.1, 0.2, 0.3]


class FakeVectorStore:
    def search(self, query_embedding, top_k):
        return [
            {
                "chunk_id": "test_1",
                "text": "Overfitting happens when a model memorizes training data.",
                "metadata": {
                    "filename": "test.pdf",
                    "page": 10,
                    "chunk_index": 0,
                },
                "distance": 0.2,
            }
        ]


def test_retrieve():
    service = RetrievalService(
        embedding_service=FakeEmbeddingService(),
        vector_store=FakeVectorStore(),
    )

    results = service.retrieve(
        "What is overfitting?",
        top_k=5,
    )

    assert len(results) == 1
    assert results[0]["chunk_id"] == "test_1"
    assert results[0]["metadata"]["page"] == 10


def test_empty_query():
    service = RetrievalService(
        embedding_service=FakeEmbeddingService(),
        vector_store=FakeVectorStore(),
    )

    try:
        service.retrieve("")
        assert False
    except ValueError:
        assert True