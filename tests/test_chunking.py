from backend.services.text_processor import (
    clean_text,
    chunk_text,
    create_document_chunks,
)


def test_clean_text():
    text = "Hello    world\n\nThis   is a test."

    result = clean_text(text)

    assert result == "Hello world This is a test."


def test_chunk_text():
    text = "A" * 2500

    chunks = chunk_text(
        text,
        chunk_size=1000,
        chunk_overlap=200,
    )

    assert len(chunks) == 4


def test_create_document_chunks():
    pages = [
        {
            "page": 1,
            "text": "Machine learning is a field of artificial intelligence."
        }
    ]

    chunks = create_document_chunks(pages)

    assert len(chunks) > 0
    assert chunks[0]["page"] == 1
    assert "text" in chunks[0]