import os
from pathlib import Path

from dotenv import load_dotenv


# Load environment variables
load_dotenv()



# Project Paths
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

UPLOAD_DIR = DATA_DIR / "uploads"

VECTOR_DB_DIR = DATA_DIR / "vector_db"

DATABASE_PATH = DATA_DIR / "studyvault.db"


# Create required directories
UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

VECTOR_DB_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# AI Configuration
GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite",
)


# Vector Database
COLLECTION_NAME = os.getenv(
    "CHROMA_COLLECTION",
    "studyvault_documents",
)


# RAG Configuration
RELEVANCE_THRESHOLD = float(
    os.getenv(
        "RELEVANCE_THRESHOLD",
        "0.8",
    )
)

# Retrieval Configuration
DEFAULT_TOP_K = int(
    os.getenv(
        "DEFAULT_TOP_K",
        "5",
    )
)

MAX_TOP_K = int(
    os.getenv(
        "MAX_TOP_K",
        "20",
    )
)


# File Upload Configuration
MAX_UPLOAD_SIZE_MB = int(
    os.getenv(
        "MAX_UPLOAD_SIZE_MB",
        "20",
    )
)

MAX_UPLOAD_SIZE_BYTES = (
    MAX_UPLOAD_SIZE_MB * 1024 * 1024
)