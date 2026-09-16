import re


def clean_text(text: str) -> str:
    """
    Clean extracted PDF text.
    """

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> list[str]:
    """
    Split text into overlapping chunks.
    """

    if not text:
        return []

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size."
        )

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - chunk_overlap

    return chunks


def create_document_chunks(
    pages: list[dict],
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> list[dict]:
    """
    Clean and chunk document pages while preserving metadata.
    """

    document_chunks = []

    for page in pages:
        page_number = page["page"]
        raw_text = page["text"]

        cleaned_text = clean_text(raw_text)

        chunks = chunk_text(
            cleaned_text,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        for chunk_index, chunk in enumerate(chunks):
            document_chunks.append(
                {
                    "page": page_number,
                    "chunk_index": chunk_index,
                    "text": chunk,
                }
            )

    return document_chunks