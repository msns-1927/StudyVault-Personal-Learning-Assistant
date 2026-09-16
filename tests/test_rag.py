from backend.services.rag_service import RAGService


class FakeRetrievalService:
    def retrieve(self, query: str, top_k: int = 5):
        return [
            {
                "chunk_id": "test_1",
                "text": (
                    "Overfitting occurs when a machine learning "
                    "model learns the training data too closely."
                ),
                "metadata": {
                    "filename": "machine_learning.pdf",
                    "page": 5,
                    "chunk_index": 0,
                },
                "distance": 0.1,
            }
        ]


class FakeLLMService:
    def generate(self, prompt: str) -> str:
        
        return (
            "Overfitting happens when a model learns the training "
            "data too closely. [Source: machine_learning.pdf, Page: 5]"
        )


def test_rag_answer():
    rag = RAGService(
        retrieval_service=FakeRetrievalService(),
        llm_service=FakeLLMService(),
    )

    result = rag.answer(
        question="What is overfitting?",
        top_k=5,
    )

    assert result["question"] == "What is overfitting?"

    assert isinstance(result["answer"], str)
    assert len(result["answer"]) > 0

    assert "[Source: machine_learning.pdf, Page: 5]" in result["answer"]

    assert result["sources"] == [
        {
            "filename": "machine_learning.pdf",
            "page": 5,
        }
    ]


# Test refusal behaviour
class IrrelevantRetrievalService:
    def retrieve(self, query: str, top_k: int = 5):
        return [
            {
                "chunk_id": "irrelevant_1",
                "text": "This document discusses neural networks.",
                "metadata": {
                    "filename": "machine_learning.pdf",
                    "page": 10,
                    "chunk_index": 0,
                },
                "distance": 1.5,
            }
        ]

def test_rag_refuses_irrelevant_question():
    rag = RAGService(
        retrieval_service=IrrelevantRetrievalService(),
        llm_service=FakeLLMService(),
    )

    result = rag.answer(
        question="What is the capital of France?",
        top_k=5,
    )

    assert "could not find enough" in result["answer"].lower()
    assert result["sources"] == []


# Duplicate-source test
class MultipleChunksRetrievalService:
    def retrieve(self, query: str, top_k: int = 5):
        return [
            {
                "chunk_id": "chunk_1",
                "text": "Overfitting is related to poor generalization.",
                "metadata": {
                    "filename": "machine_learning.pdf",
                    "page": 5,
                    "chunk_index": 0,
                },
                "distance": 0.1,
            },
            {
                "chunk_id": "chunk_2",
                "text": "A model can memorize training data.",
                "metadata": {
                    "filename": "machine_learning.pdf",
                    "page": 5,
                    "chunk_index": 1,
                },
                "distance": 0.2,
            },
            {
                "chunk_id": "chunk_3",
                "text": "Regularization can help reduce overfitting.",
                "metadata": {
                    "filename": "machine_learning.pdf",
                    "page": 6,
                    "chunk_index": 0,
                },
                "distance": 0.3,
            },
        ]


def test_rag_deduplicates_sources():
    rag = RAGService(
        retrieval_service=MultipleChunksRetrievalService(),
        llm_service=FakeLLMService(),
    )

    result = rag.answer(
        question="What is overfitting?",
        top_k=5,
    )

    assert result["sources"] == [
        {
            "filename": "machine_learning.pdf",
            "page": 5,
        },
        {
            "filename": "machine_learning.pdf",
            "page": 6,
        },
    ]


def test_rag_rejects_irrelevant_question():
    class FakeRetrievalService:
        def retrieve(
            self,
            query: str,
            top_k: int = 5,
        ) -> list[dict]:
            return [
                {
                    "chunk_id": "irrelevant_chunk",
                    "text": "Some unrelated document content.",
                    "metadata": {
                        "document_id": "test_document",
                        "filename": "test.pdf",
                        "page": 1,
                        "chunk_index": 0,
                    },
                    "distance": 1.2,
                }
            ]

    class FakeLLMService:
        def generate(self, prompt: str) -> str:
            raise AssertionError(
                "LLM should not be called for irrelevant context."
            )

    from backend.services.rag_service import RAGService

    rag_service = RAGService(
        retrieval_service=FakeRetrievalService(),
        llm_service=FakeLLMService(),
    )

    result = rag_service.answer(
        question="What is the capital of Japan?",
        top_k=5,
    )

    assert (
        "could not find enough relevant information"
        in result["answer"].lower()
    )

    assert result["sources"] == []



def test_rag_answers_relevant_question():

    class FakeRetrievalService:
        def retrieve(
            self,
            query: str,
            top_k: int = 5,
        ) -> list[dict]:

            return [
                {
                    "chunk_id": "relevant_chunk",
                    "text": (
                        "Supervised learning uses "
                        "labeled training data."
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

    class FakeLLMService:
        def generate(self, prompt: str) -> str:
            return (
                "Supervised learning uses labeled "
                "training data."
            )

    from backend.services.rag_service import RAGService

    rag_service = RAGService(
        retrieval_service=FakeRetrievalService(),
        llm_service=FakeLLMService(),
    )

    result = rag_service.answer(
        question="What is supervised learning?",
        top_k=5,
    )

    assert (
        result["answer"]
        == (
            "Supervised learning uses labeled "
            "training data."
        )
    )

    assert len(result["sources"]) == 1

    assert (
        result["sources"][0]["filename"]
        == "machine_learning.pdf"
    )

    assert result["sources"][0]["page"] == 5


def test_rag_empty_question():

    class FakeRetrievalService:
        pass

    class FakeLLMService:
        pass

    from backend.services.rag_service import RAGService

    rag_service = RAGService(
        retrieval_service=FakeRetrievalService(),
        llm_service=FakeLLMService(),
    )

    try:

        rag_service.answer(
            question="",
            top_k=5,
        )

        assert False, (
            "Expected ValueError "
            "for empty question."
        )

    except ValueError as exc:

        assert (
            str(exc)
            == "Question cannot be empty."
        )