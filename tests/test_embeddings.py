# Embedding test
from backend.services.embedding_service import EmbeddingService


def test_single_embedding():
    service = EmbeddingService()

    text = "Machine learning is a field of artificial intelligence."

    embedding = service.generate_embedding(text)

    assert isinstance(embedding, list)
    assert len(embedding) == 384


def test_multiple_embeddings():
    service = EmbeddingService()

    texts = [
        "Machine learning is a field of artificial intelligence.",
        "Deep learning uses neural networks.",
        "Overfitting occurs when a model memorizes training data.",
    ]

    embeddings = service.generate_embeddings(texts)

    assert len(embeddings) == 3
    assert all(len(embedding) == 384 for embedding in embeddings)



# Semantic similarity test
import numpy as np
from backend.services.embedding_service import EmbeddingService


def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:
    """
    Calculate cosine similarity between two vectors.
    """

    a = np.array(vector_a)
    b = np.array(vector_b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


def test_semantic_similarity():
    service = EmbeddingService()

    text_a = "A machine learning model is overfitting."
    text_b = "The model memorizes the training data."
    text_c = "The weather is sunny today."

    embedding_a = service.generate_embedding(text_a)
    embedding_b = service.generate_embedding(text_b)
    embedding_c = service.generate_embedding(text_c)

    similarity_ab = cosine_similarity(
        embedding_a,
        embedding_b,
    )

    similarity_ac = cosine_similarity(
        embedding_a,
        embedding_c,
    )

    assert similarity_ab > similarity_ac