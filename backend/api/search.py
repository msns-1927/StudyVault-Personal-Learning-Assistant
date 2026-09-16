from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.services.retrieval_service import RetrievalService


router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


retrieval_service = RetrievalService()


class SearchRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        description="Question or search query.",
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of chunks to retrieve.",
    )


@router.post("")
def search_documents(request: SearchRequest):
    """
    Retrieve relevant document chunks.
    """

    try:
        results = retrieval_service.retrieve(
            query=request.query,
            top_k=request.top_k,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    return {
        "query": request.query,
        "results": results,
    }