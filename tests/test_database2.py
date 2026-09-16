import sqlite3

import pytest

import backend.services.database as database


@pytest.fixture
def isolated_database(tmp_path, monkeypatch):

    test_database_path = (
        tmp_path / "test_studyvault.db"
    )

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        test_database_path,
    )

    database.initialize_database()

    return test_database_path


def test_create_conversation(isolated_database,):
    conversation_id = database.create_conversation(
        title="Test Conversation"
    )

    assert isinstance(
        conversation_id,
        int,
    )

    conversation = database.get_conversation(
        conversation_id
    )

    assert conversation is not None

    assert (
        conversation["title"]
        == "Test Conversation"
    )


def test_add_and_get_messages(isolated_database,):
    conversation_id = database.create_conversation(
        title="Message Test"
    )

    user_message_id = database.add_message(
        conversation_id=conversation_id,
        role="user",
        content="What is machine learning?",
    )

    assistant_message_id = database.add_message(
        conversation_id=conversation_id,
        role="assistant",
        content="Machine learning is a field of AI.",
    )

    assert isinstance(
        user_message_id,
        int,
    )

    assert isinstance(
        assistant_message_id,
        int,
    )

    messages = database.get_messages(
        conversation_id
    )

    assert len(messages) == 2

    assert messages[0]["role"] == "user"

    assert (
        messages[0]["content"]
        == "What is machine learning?"
    )

    assert (
        messages[1]["role"]
        == "assistant"
    )


def test_invalid_message_role(isolated_database,):
    conversation_id = database.create_conversation(
        title="Invalid Role Test"
    )

    try:
        database.add_message(
            conversation_id=conversation_id,
            role="system",
            content="Invalid message",
        )

        assert False, (
            "Expected ValueError "
            "for invalid role."
        )

    except ValueError as exc:

        assert (
            str(exc)
            == "Role must be 'user' or 'assistant'."
        )


def test_nonexistent_conversation(isolated_database,):
    conversation = database.get_conversation(
        999999999
    )

    assert conversation is None


def test_generate_conversation_title(isolated_database,):

    title = database.generate_conversation_title(
        "What is supervised learning?"
    )

    assert (
        title
        == "What is supervised learning?"
    )


def test_long_conversation_title(isolated_database,):

    question = (
        "This is a very long question that "
        "should be shortened when converted "
        "into a conversation title because "
        "the original question is too long."
    )

    title = database.generate_conversation_title(
        question
    )

    assert len(title) <= 50

    assert title.endswith("...")


def test_empty_conversation_title(isolated_database,):

    title = database.generate_conversation_title(
        ""
    )

    assert title == "New Conversation"