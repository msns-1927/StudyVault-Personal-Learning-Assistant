import uuid

from backend.services.vector_store import VectorStore


def test_vector_store():
    collection_name = f"test_{uuid.uuid4().hex}"

    store = VectorStore(
        collection_name=collection_name
    )

    document_id = f"test_{uuid.uuid4()}"

    chunks = [
        {
            "page": 1,
            "chunk_index": 0,
            "text": "Machine learning is a field of artificial intelligence.",
        },
        {
            "page": 2,
            "chunk_index": 0,
            "text": "Deep learning uses neural networks.",
        },
    ]

    # ChromaDB must receive embeddings with the same
    # dimension as our production embedding model.
    embeddings = [
        [0.1] * 384,
        [0.2] * 384,
    ]

    added = store.add_chunks(
        chunks=chunks,
        embeddings=embeddings,
        document_id=document_id,
        filename="test.pdf",
    )

    assert added == 2
    assert store.count() == 2