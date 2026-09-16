from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.services.database import (
    create_conversation,
    delete_conversation,
    generate_conversation_title,
    get_conversation,
    get_conversations,
    get_messages,
    update_conversation_title,
)


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


class ConversationUpdate(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )


@router.post("")
def create_new_conversation():
    """
    Create a new conversation.
    """

    conversation_id = create_conversation()

    return get_conversation(
        conversation_id
    )


@router.get("")
def list_conversations():
    """
    Return all conversations.
    """

    return {
        "conversations": get_conversations()
    }


@router.get("/{conversation_id}")
def get_conversation_details(
    conversation_id: int,
):
    """
    Return conversation metadata.
    """

    conversation = get_conversation(
        conversation_id
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    return conversation


@router.get("/{conversation_id}/messages")
def get_conversation_messages(
    conversation_id: int,
):
    """
    Return all messages for a conversation.
    """

    conversation = get_conversation(
        conversation_id
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    return {
        "conversation_id": conversation_id,
        "messages": get_messages(
            conversation_id
        ),
    }


@router.patch("/{conversation_id}")
def rename_conversation(
    conversation_id: int,
    request: ConversationUpdate,
):
    """
    Rename an existing conversation.
    """

    conversation = get_conversation(
        conversation_id
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    try:
        updated = update_conversation_title(
            conversation_id=conversation_id,
            title=request.title,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    return get_conversation(
        conversation_id
    )


@router.delete("/{conversation_id}")
def remove_conversation(
    conversation_id: int,
):
    """
    Delete a conversation and all its messages.
    """

    conversation = get_conversation(
        conversation_id
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    deleted = delete_conversation(
        conversation_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    return {
        "message": "Conversation deleted successfully.",
        "conversation_id": conversation_id,
    }