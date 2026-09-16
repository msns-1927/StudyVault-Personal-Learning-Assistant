from pathlib import Path
from uuid import uuid4
import hashlib
import logging

from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.config import (
    MAX_UPLOAD_SIZE_BYTES,
    MAX_UPLOAD_SIZE_MB,
    UPLOAD_DIR,
)
from backend.services.database import (
    add_document,
    delete_document_record,
    get_document,
    get_documents,
)
from backend.services.pdf_processor import extract_text_from_pdf
from backend.services.text_processor import create_document_chunks
from backend.services.embedding_service import EmbeddingService
from backend.services.vector_store import VectorStore


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


embedding_service = EmbeddingService()
vector_store = VectorStore()


def calculate_file_hash(file_content: bytes) -> str:
    """
    Calculate a SHA-256 hash for the uploaded file.
    """
    return hashlib.sha256(file_content).hexdigest()


def document_exists(filename: str) -> bool:
    """
    Check whether a document with the same filename
    already exists.
    """
    documents = get_documents()

    return any(
        document["filename"].lower() == filename.lower()
        for document in documents
    )


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a PDF, process it, generate embeddings,
    store vectors, and save document metadata.
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file name provided.",
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are currently supported.",
        )

    safe_filename = Path(file.filename).name

    if document_exists(safe_filename):
        logger.warning(
            "Duplicate document upload rejected: filename=%s",
            safe_filename,
        )

        raise HTTPException(
            status_code=409,
            detail="A document with this filename already exists.",
        )

    document_id = str(uuid4())

    file_content = await file.read()

    if not file_content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty.",
        )

    if len(file_content) > MAX_UPLOAD_SIZE_BYTES:
        logger.warning(
            "File upload rejected: filename=%s size_mb=%.2f",
            safe_filename,
            len(file_content) / (1024 * 1024),
        )

        raise HTTPException(
            status_code=413,
            detail=(
                f"File is too large. "
                f"Maximum allowed size is "
                f"{MAX_UPLOAD_SIZE_MB} MB."
            ),
        )

    file_hash = calculate_file_hash(
        file_content
    )

    if vector_store.document_hash_exists(file_hash):
        logger.warning(
            "Duplicate document rejected by hash: "
            "filename=%s hash=%s",
            safe_filename,
            file_hash,
        )

        raise HTTPException(
            status_code=409,
            detail="This document has already been uploaded.",
        )

    file_path = (
        UPLOAD_DIR
        / f"{document_id}_{safe_filename}"
    )

    logger.info(
        "Starting document upload: "
        "filename=%s document_id=%s",
        safe_filename,
        document_id,
    )

    with open(file_path, "wb") as output_file:
        output_file.write(file_content)

    try:
        # Extract text
        pages = extract_text_from_pdf(
            str(file_path)
        )

        # Create chunks
        chunks = create_document_chunks(
            pages
        )

        # Extract chunk text
        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        # Generate embeddings
        embeddings = embedding_service.generate_embeddings(
            texts
        )

        # Store vectors
        stored_chunks = vector_store.add_chunks(
            chunks=chunks,
            embeddings=embeddings,
            document_id=document_id,
            filename=safe_filename,
            file_hash=file_hash,
        )

        # Store document metadata in SQLite
        add_document(
            document_id=document_id,
            filename=safe_filename,
            file_hash=file_hash,
            file_path=str(file_path),
            pages=len(pages),
            chunks=stored_chunks,
        )

        logger.info(
            "Document processed successfully: "
            "filename=%s pages=%d chunks=%d",
            safe_filename,
            len(pages),
            stored_chunks,
        )

    except Exception:
        logger.exception(
            "Failed to process PDF: "
            "filename=%s document_id=%s",
            safe_filename,
            document_id,
        )

        # Remove vectors if they were created
        try:
            vector_store.delete_document(
                document_id
            )
        except Exception:
            logger.exception(
                "Failed to clean up vector data: "
                "document_id=%s",
                document_id,
            )

        # Remove SQLite metadata if it was created
        try:
            delete_document_record(
                document_id
            )
        except Exception:
            logger.exception(
                "Failed to clean up database record: "
                "document_id=%s",
                document_id,
            )

        # Remove physical PDF
        file_path.unlink(
            missing_ok=True
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to process PDF.",
        )

    return {
        "message": "Document uploaded successfully.",
        "document_id": document_id,
        "filename": safe_filename,
        "pages": len(pages),
        "chunks": stored_chunks,
    }


@router.get("")
def list_documents():
    """
    Return all uploaded documents.
    """

    documents = get_documents()

    logger.info(
        "Retrieved uploaded documents: count=%d",
        len(documents),
    )

    return {
        "documents": documents,
        "total_documents": len(documents),
    }


@router.delete("/{document_id}")
def delete_document(document_id: str):
    """
    Delete a document from SQLite, ChromaDB,
    and the uploads directory.
    """

    document = get_document(
        document_id
    )

    if document is None:
        logger.warning(
            "Document not found for deletion: "
            "document_id=%s",
            document_id,
        )

        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    filename = document["filename"]
    file_path = Path(
        document["file_path"]
    )

    # Delete vectors
    deleted_chunks = vector_store.delete_document(
        document_id
    )

    # Delete SQLite record
    database_deleted = delete_document_record(
        document_id
    )

    # Delete physical file
    file_deleted = False

    if file_path.exists():
        file_path.unlink()
        file_deleted = True

    logger.info(
        "Document deleted: "
        "document_id=%s filename=%s "
        "chunks=%d database_deleted=%s "
        "file_deleted=%s",
        document_id,
        filename,
        deleted_chunks,
        database_deleted,
        file_deleted,
    )

    return {
        "message": "Document deleted successfully.",
        "document_id": document_id,
        "filename": filename,
        "deleted_chunks": deleted_chunks,
        "database_deleted": database_deleted,
        "file_deleted": file_deleted,
    }