from fastapi import FastAPI

from backend.logging_config import setup_logging
from backend.services.database import initialize_database

from backend.api.documents import router as documents_router
from backend.api.search import router as search_router
from backend.api.ask import router as ask_router
from backend.services.database import initialize_database
from backend.api.conversations import (
    router as conversations_router,
)

setup_logging()
initialize_database()


app = FastAPI(
    title="StudyVault API",
    description="RAG-powered personal learning assistant",
    version="1.0.0",
)

app.include_router(documents_router)
app.include_router(search_router)
app.include_router(ask_router)
app.include_router(conversations_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to StudyVault",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }