from io import BytesIO

import pytest
from fastapi.testclient import TestClient
from reportlab.pdfgen import canvas

from backend.main import app
from backend.api import documents


def create_test_pdf():
    """
    Create a small PDF in memory for testing.
    """

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer)

    pdf.drawString(
        100,
        750,
        "Machine Learning Test Document",
    )

    pdf.drawString(
        100,
        700,
        "Supervised learning uses labeled data.",
    )

    pdf.drawString(
        100,
        650,
        "Unsupervised learning works with unlabeled data.",
    )

    pdf.save()

    buffer.seek(0)

    return buffer


@pytest.fixture
def isolated_document_environment(
    tmp_path,
):
    """
    Use temporary storage for document API tests.
    """

    original_upload_dir = (
        documents.UPLOAD_DIR
    )

    original_vector_store = (
        documents.vector_store
    )

    test_upload_dir = (
        tmp_path / "uploads"
    )

    test_vector_db = (
        tmp_path / "vector_db"
    )

    test_upload_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    documents.UPLOAD_DIR = (
        test_upload_dir
    )

    documents.vector_store = (
        documents.VectorStore(
            collection_name=(
                "test_documents"
            ),
            chroma_path=str(
                test_vector_db
            ),
        )
    )

    yield

    documents.UPLOAD_DIR = (
        original_upload_dir
    )

    documents.vector_store = (
        original_vector_store
    )


@pytest.fixture
def client(
    isolated_document_environment,
):
    return TestClient(app)


def test_pdf_upload(client):

    pdf = create_test_pdf()

    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "test_machine_learning.pdf",
                pdf,
                "application/pdf",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["message"]
        == "Document uploaded successfully."
    )

    assert (
        data["filename"]
        == "test_machine_learning.pdf"
    )

    assert "document_id" in data

    assert data["pages"] >= 1

    assert data["chunks"] >= 1


def test_non_pdf_upload(client):

    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "test.txt",
                b"This is not a PDF.",
                "text/plain",
            )
        },
    )

    assert response.status_code == 400

    assert (
        response.json()["detail"]
        == "Only PDF files are currently supported."
    )


def test_upload_without_filename(client):

    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "",
                b"some content",
                "application/pdf",
            )
        },
    )

    assert response.status_code == 422


def test_upload_empty_pdf(client):

    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "empty.pdf",
                b"",
                "application/pdf",
            )
        },
    )

    assert response.status_code == 500

    assert "Failed to process PDF" in (
        response.json()["detail"]
    )


def test_delete_document(client):

    pdf = create_test_pdf()

    upload_response = client.post(
        "/documents/upload",
        files={
            "file": (
                "delete_test.pdf",
                pdf,
                "application/pdf",
            )
        },
    )

    assert upload_response.status_code == 200

    document_id = (
        upload_response.json()["document_id"]
    )

    delete_response = client.delete(
        f"/documents/{document_id}"
    )

    assert delete_response.status_code == 200

    delete_data = delete_response.json()

    assert (
        delete_data["message"]
        == "Document deleted successfully."
    )

    assert (
        delete_data["document_id"]
        == document_id
    )

    assert (
        delete_data["deleted_chunks"] >= 1
    )

    documents_response = client.get(
        "/documents"
    )

    assert documents_response.status_code == 200

    documents = (
        documents_response.json()["documents"]
    )

    document_ids = [
        document["document_id"]
        for document in documents
    ]

    assert document_id not in document_ids



def test_delete_nonexistent_document(client):

    response = client.delete(
        "/documents/nonexistent-document-id"
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Document not found."
    )