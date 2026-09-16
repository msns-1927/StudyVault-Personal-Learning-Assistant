import sqlite3

from backend.config import DATABASE_PATH


def get_connection():
    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (conversation_id)
                REFERENCES conversations(id)
        )
        """
    )

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id TEXT UNIQUE NOT NULL,
            filename TEXT NOT NULL,
            file_hash TEXT UNIQUE NOT NULL,
            file_path TEXT NOT NULL,
            pages INTEGER NOT NULL,
            chunks INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'processed',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def create_conversation(title: str = "New Conversation") -> int:
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO conversations (title)
        VALUES (?)
        """,
        (title,),
    )

    conversation_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return conversation_id


def add_message(
    conversation_id: int,
    role: str,
    content: str,
) -> int:
    if role not in {"user", "assistant"}:
        raise ValueError(
            "Role must be 'user' or 'assistant'."
        )

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO messages (
            conversation_id,
            role,
            content
        )
        VALUES (?, ?, ?)
        """,
        (
            conversation_id,
            role,
            content,
        ),
    )

    message_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return message_id


def get_messages(
    conversation_id: int,
) -> list[dict]:
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            conversation_id,
            role,
            content,
            created_at
        FROM messages
        WHERE conversation_id = ?
        ORDER BY id ASC
        """,
        (conversation_id,),
    )

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]


def get_conversations() -> list[dict]:
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            title,
            created_at
        FROM conversations
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]


def get_conversation(
    conversation_id: int,
) -> dict | None:
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            title,
            created_at
        FROM conversations
        WHERE id = ?
        """,
        (conversation_id,),
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return dict(row)


def generate_conversation_title(question: str) -> str:
    title = " ".join(question.strip().split())

    if not title:
        return "New Conversation"

    if len(title) <= 50:
        return title

    return title[:47].rstrip() + "..."


def add_document(
    document_id: str,
    filename: str,
    file_hash: str,
    file_path: str,
    pages: int,
    chunks: int,
) -> int:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO documents (
            document_id,
            filename,
            file_hash,
            file_path,
            pages,
            chunks,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            document_id,
            filename,
            file_hash,
            file_path,
            pages,
            chunks,
            "processed",
        ),
    )

    document_database_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return document_database_id


def get_documents() -> list[dict]:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            document_id,
            filename,
            file_hash,
            file_path,
            pages,
            chunks,
            status,
            created_at
        FROM documents
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]


def get_document(
    document_id: str,
) -> dict | None:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            document_id,
            filename,
            file_hash,
            file_path,
            pages,
            chunks,
            status,
            created_at
        FROM documents
        WHERE document_id = ?
        """,
        (document_id,),
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return dict(row)


def delete_document_record(
    document_id: str,
) -> bool:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM documents
        WHERE document_id = ?
        """,
        (document_id,),
    )

    deleted = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return deleted


def update_conversation_title(
    conversation_id: int,
    title: str,
) -> bool:
    """
    Update the title of an existing conversation.
    """

    title = " ".join(title.strip().split())

    if not title:
        raise ValueError(
            "Conversation title cannot be empty."
        )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE conversations
        SET title = ?
        WHERE id = ?
        """,
        (title, conversation_id),
    )

    updated = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return updated


def delete_conversation(
    conversation_id: int,
) -> bool:
    """
    Delete a conversation and all of its messages.
    """

    connection = get_connection()
    cursor = connection.cursor()

    # Delete messages first because they reference
    # the conversation.
    cursor.execute(
        """
        DELETE FROM messages
        WHERE conversation_id = ?
        """,
        (conversation_id,),
    )

    cursor.execute(
        """
        DELETE FROM conversations
        WHERE id = ?
        """,
        (conversation_id,),
    )

    deleted = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return deleted