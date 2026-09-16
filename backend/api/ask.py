from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.services.database import (
    add_message,
    create_conversation,
    generate_conversation_title,
    get_conversation,
)

from backend.services.rag_service import RAGService


router = APIRouter(
    prefix="/ask",
    tags=["RAG"],
)

rag_service = RAGService()


class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="Question to ask about uploaded documents.",
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of relevant chunks to retrieve.",
    )

    conversation_id: int | None = Field(
       default=None,
       description="Existing conversation ID.",
    )

    study_mode: str = Field(
        default="explain",
        description="Study mode.",
    )


@router.post("")
def ask_question(request: AskRequest):
    try:
        conversation_id = request.conversation_id

        # Create a new conversation if one was not provided.
        if conversation_id is None:
            conversation_id = create_conversation(
                title=generate_conversation_title(
                    request.question
                )
            )

        else:
            # Make sure the requested conversation exists.
            conversation = get_conversation(
                conversation_id
            )

            if conversation is None:
                raise HTTPException(
                    status_code=404,
                    detail="Conversation not found.",
                )

        # Generate the RAG answer using conversation history.
        result = rag_service.answer(
            question=request.question,
            top_k=request.top_k,
            conversation_id=conversation_id,
            study_mode=request.study_mode,
        )

        # Save the user's question.
        add_message(
            conversation_id=conversation_id,
            role="user",
            content=request.question,
        )

        # Save the assistant's answer.
        add_message(
            conversation_id=conversation_id,
            role="assistant",
            content=result["answer"],
        )

        return {
            "conversation_id": conversation_id,
            **result,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )