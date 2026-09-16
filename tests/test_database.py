from backend.services.database import (
    add_message,
    create_conversation,
    get_connection,
    get_conversation,
    get_conversations,
    get_messages,
    initialize_database,
    generate_conversation_title,
)


def test_database_initialization(tmp_path, monkeypatch):
    import backend.services.database as database

    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        test_database,
    )

    initialize_database()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        """
    )

    tables = {
        row["name"]
        for row in cursor.fetchall()
    }

    connection.close()

    assert "conversations" in tables
    assert "messages" in tables



def test_conversation_and_messages(tmp_path, monkeypatch):
    import backend.services.database as database

    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        test_database,
    )

    initialize_database()

    conversation_id = create_conversation(
        title="Machine Learning Discussion"
    )

    assert isinstance(conversation_id, int)

    user_message_id = add_message(
        conversation_id=conversation_id,
        role="user",
        content="What is overfitting?",
    )

    assistant_message_id = add_message(
        conversation_id=conversation_id,
        role="assistant",
        content="Overfitting occurs when a model learns the training data too closely.",
    )

    assert isinstance(user_message_id, int)
    assert isinstance(assistant_message_id, int)

    messages = get_messages(
        conversation_id=conversation_id
    )

    assert len(messages) == 2

    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "What is overfitting?"

    assert messages[1]["role"] == "assistant"
    assert "training data" in messages[1]["content"]



def test_get_conversations(tmp_path, monkeypatch):
    import backend.services.database as database

    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        test_database,
    )

    initialize_database()

    first_id = create_conversation(
        title="First Conversation"
    )

    second_id = create_conversation(
        title="Second Conversation"
    )

    conversations = get_conversations()

    assert len(conversations) == 2

    assert conversations[0]["id"] == second_id
    assert conversations[0]["title"] == "Second Conversation"

    assert conversations[1]["id"] == first_id
    assert conversations[1]["title"] == "First Conversation"


def test_get_conversation(tmp_path, monkeypatch):
    import backend.services.database as database

    test_database = tmp_path / "test.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        test_database,
    )

    initialize_database()

    conversation_id = create_conversation(
        title="Machine Learning"
    )

    conversation = get_conversation(
        conversation_id
    )

    assert conversation is not None
    assert conversation["id"] == conversation_id
    assert conversation["title"] == "Machine Learning"

    missing = get_conversation(9999)

    assert missing is None


def test_generate_conversation_title():
    assert (
        generate_conversation_title(
            "What is overfitting?"
        )
        == "What is overfitting?"
    )

    assert (
        generate_conversation_title(
            "   What   is   overfitting?   "
        )
        == "What is overfitting?"
    )

    assert (
        generate_conversation_title("")
        == "New Conversation"
    )


def test_generate_long_conversation_title():
    question = (
        "Explain the difference between supervised "
        "and unsupervised learning in machine learning "
        "with examples"
    )

    title = generate_conversation_title(question)

    assert len(title) <= 50
    assert title.endswith("...")