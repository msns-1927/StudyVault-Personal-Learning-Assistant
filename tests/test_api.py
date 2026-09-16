from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "running"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


def test_list_documents():
    response = client.get("/documents")

    assert response.status_code == 200

    data = response.json()

    assert "documents" in data
    assert "total_documents" in data

    assert isinstance(
        data["documents"],
        list,
    )


def test_list_conversations():
    response = client.get("/conversations")

    assert response.status_code == 200

    data = response.json()

    assert "conversations" in data

    assert isinstance(
        data["conversations"],
        list,
    )


def test_search_empty_query():
    response = client.post(
        "/search",
        json={
            "query": "",
            "top_k": 5,
        },
    )

    assert response.status_code == 422


def test_ask_empty_question():
    response = client.post(
        "/ask",
        json={
            "question": "",
            "top_k": 5,
        },
    )

    assert response.status_code == 422


def test_nonexistent_conversation():
    response = client.get(
        "/conversations/999999999/messages"
    )

    assert response.status_code == 404


def test_search_invalid_top_k():

    response = client.post(
        "/search",
        json={
            "query": "machine learning",
            "top_k": 0,
        },
    )

    assert response.status_code == 422


def test_search_top_k_above_limit():

    response = client.post(
        "/search",
        json={
            "query": "machine learning",
            "top_k": 21,
        },
    )

    assert response.status_code == 422


def test_get_nonexistent_conversation():

    response = client.get(
        "/conversations/999999999"
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Conversation not found."
    )


def test_get_messages_for_nonexistent_conversation():

    response = client.get(
        "/conversations/999999999/messages"
    )

    assert response.status_code == 404

    assert (
        response.json()["detail"]
        == "Conversation not found."
    )


def test_search_invalid_top_k():
    response = client.post(
        "/search",
        json={
            "query": "machine learning",
            "top_k": 0,
        },
    )

    assert response.status_code == 422


def test_search_top_k_above_limit():
    response = client.post(
        "/search",
        json={
            "query": "machine learning",
            "top_k": 21,
        },
    )

    assert response.status_code == 422