# 📚 StudyVault-Personal-Learning-Assistant

## 🚀 Overview:

StudyVault is a RAG-powered Personal Learning Assistant that helps students learn from their own study materials. Users can upload PDF documents, ask questions about their content, and receive clear, context-aware answers generated using Retrieval-Augmented Generation (RAG) with Gemini.

The system processes uploaded documents through text extraction, cleaning, chunking, semantic embeddings, and vector storage using ChromaDB. When a user asks a question, StudyVault retrieves the most relevant content from the uploaded documents and provides an answer with source and page citations, helping users understand and verify the information.

StudyVault also includes conversation history, document management, semantic search, relevance filtering, and multiple Study Modes such as Explain, Summary, Quiz, Flashcards, and Key Points, providing an interactive learning experience through a Streamlit frontend and FastAPI backend.


## ✨ Features:

- 📄 **Document Upload & Processing** — Upload PDF study materials and automatically extract and process their content.
- 🧹 **Text Cleaning & Chunking** — Cleans extracted text and divides documents into meaningful overlapping chunks for efficient retrieval.
- 🧠 **Semantic Embeddings** — Converts document chunks and user queries into vector representations using Sentence Transformers.
- 🗄️ **Vector Database** — Stores document embeddings and metadata in ChromaDB for fast semantic similarity search.
- 🔎 **Semantic Search** — Retrieves the most relevant document content based on the meaning of the user's question rather than simple keyword matching.
- 🤖 **RAG-Based Question Answering** — Combines retrieved document context with Gemini to generate context-aware answers.
- 📚 **Source & Page Citations** — Provides document filenames and page numbers with answers to make information easier to verify.
- 🛡️ **Hallucination Control** — Uses relevance filtering and context-restricted prompting to avoid generating unsupported answers.
- 💬 **Conversation History** — Maintains previous questions and answers using SQLite for context-aware conversations.
- 🗂️ **Conversation Management** — Create, view, rename, and delete conversations.
- 📑 **Document Management** — View uploaded documents and delete documents along with their associated vector data and metadata.
- 🔐 **Duplicate Document Detection** — Prevents duplicate uploads using filename checks and SHA-256 file hashing.
- 📦 **File Validation** — Validates uploaded files and enforces configurable file-size limits.
- 🎓 **Study Modes** — Provides multiple learning modes such as:
  - **Explain** — Understand a concept in a simple and structured way.
  - **Summary** — Generate concise summaries from the study material.
  - **Quiz** — Practice concepts through questions.
  - **Flashcards** — Create quick revision cards.
  - **Key Points** — Extract important concepts and takeaways.
- ⚡ **FastAPI Backend** — Provides a structured REST API for document processing, retrieval, RAG, search, and conversation management.
- 🖥️ **Streamlit Interface** — Provides an interactive user interface for uploading documents, asking questions, managing conversations, and using Study Modes.
- ⚙️ **Configurable Architecture** — Centralized configuration for models, retrieval settings, upload limits, and database/vector-store paths.
- 📝 **Application Logging** — Includes structured logging for monitoring document processing and application operations.



## 🎓 Study Modes:

StudyVault provides multiple AI-powered Study Modes to help users learn and revise information from their uploaded study materials.

### 📖 Explain:

Provides a clear and easy-to-understand explanation of a selected concept using the information retrieved from the uploaded documents.

### 📝 Summary:

Generates a concise summary of the relevant study material, focusing on the main concepts and important information.

### 🧠 Quiz:

Generates practice questions based on the uploaded study materials to help users test their understanding and reinforce learning.

### 🃏 Flashcards:

Creates quick question-and-answer style flashcards from the relevant study content for efficient revision and memorization.

### 🔑 Key Points:

Extracts the most important concepts, facts, and takeaways from the retrieved study material for quick revision.

### 🔄 RAG-Powered Learning:

All Study Modes are integrated with the StudyVault RAG pipeline, allowing the learning content to be generated from the user's uploaded documents rather than relying solely on general-purpose knowledge.




## 🏗️ Architecture:

StudyVault follows a modular **Retrieval-Augmented Generation (RAG)** architecture that combines document processing, semantic search, vector storage, conversational memory, and Large Language Model (LLM) generation.

### System Architecture:

```text
                         ┌──────────────────────┐
                         │      User / Student  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Streamlit Frontend │
                         │                      │
                         │ • Document Upload   │
                         │ • Chat Interface    │
                         │ • Study Modes       │
                         │ • Conversations     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    FastAPI Backend   │
                         │                      │
                         │ • Document API      │
                         │ • Search API        │
                         │ • Ask API           │
                         │ • Conversation API  │
                         └──────────┬───────────┘
                                    │
                  ┌─────────────────┼─────────────────┐
                  │                 │                 │
                  ▼                 ▼                 ▼
        ┌─────────────────┐ ┌───────────────┐ ┌─────────────────┐
        │ Document        │ │ RAG /         │ │ Conversation    │
        │ Processing      │ │ Retrieval     │ │ Management      │
        │                 │ │               │ │                 │
        │ • PDF Extract   │ │ • Embeddings  │ │ • SQLite        │
        │ • Cleaning      │ │ • Search      │ │ • History       │
        │ • Chunking      │ │ • Relevance   │ │ • Messages      │
        └────────┬────────┘ │ • Prompting   │ └─────────────────┘
                 │          └───────┬───────┘
                 │                  │
                 ▼                  ▼
        ┌─────────────────┐ ┌─────────────────┐
        │ Sentence        │ │    ChromaDB     │
        │ Transformers    │ │                 │
        │                 │ │ Vector Storage  │
        │ Embeddings      │ │ + Metadata      │
        └────────┬────────┘ └────────┬────────┘
                 │                   │
                 └─────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │    Gemini LLM    │
                  │                  │
                  │ Context-Aware    │
                  │ Answer Generation│
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Final Response   │
                  │                  │
                  │ • Answer         │
                  │ • Sources        │
                  │ • Page Numbers   │
                  └──────────────────┘
```
### 🔄 RAG Pipeline:

```
PDF Document
     │
     ▼
Text Extraction
     │
     ▼
Text Cleaning
     │
     ▼
Text Chunking
     │
     ▼
Embedding Generation
     │
     ▼
ChromaDB Vector Store
     │
     │
     │        User Question
     │              │
     │              ▼
     │       Query Embedding
     │              │
     └──────────────┤
                    ▼
             Similarity Search
                    │
                    ▼
             Relevant Chunks
                    │
                    ▼
             Relevance Check
                    │
                    ▼
             Context + Question
                    │
                    ▼
                Gemini LLM
                    │
                    ▼
          Answer + Source Citations
```

### 🧩 Major Components:

| Component | Responsibility |
|---|---|
| **Streamlit** | Provides the interactive user interface |
| **FastAPI** | Handles backend REST APIs and application logic |
| **PDF Processor** | Extracts text from uploaded PDF documents |
| **Text Processor** | Cleans and splits extracted text into chunks |
| **Embedding Service** | Generates vector embeddings using Sentence Transformers |
| **ChromaDB** | Stores document embeddings and metadata for semantic retrieval |
| **Retrieval Service** | Finds relevant document chunks for a user query |
| **RAG Service** | Combines retrieved context, conversation history, and user questions |
| **Gemini LLM** | Generates context-aware responses |
| **SQLite** | Stores conversations, messages, and document metadata |
| **Study Modes** | Provides Explain, Summary, Quiz, Flashcards, and Key Points learning workflows |


### 🔁 Query Flow:

When a user asks a question, StudyVault follows these steps:

- The question is received through the Streamlit interface.
- FastAPI sends the question to the RAG service.
- The question is converted into an embedding.
- ChromaDB performs semantic similarity search.
- Relevant document chunks are retrieved.
- Retrieved context is checked for relevance.
- The relevant context and conversation history are provided to Gemini.
- Gemini generates an answer using the available document context.
- StudyVault returns the answer along with document and page-level sources.


## 🛠️ Tech Stack:

| Category | Technologies |
|---|---|
| **Programming Language** | Python |
| **Backend Framework** | FastAPI |
| **Frontend Framework** | Streamlit |
| **LLM** | Google Gemini |
| **RAG Framework** | Custom RAG Pipeline |
| **Embedding Model** | Sentence Transformers (`all-MiniLM-L6-v2`) |
| **Vector Database** | ChromaDB |
| **Database** | SQLite |
| **Document Processing** | PyMuPDF |
| **Data Validation** | Pydantic |
| **Machine Learning / NLP** | Sentence Transformers, Semantic Search |
| **API Communication** | REST API |
| **Testing** | pytest, pytest-cov |
| **Configuration** | python-dotenv |
| **Version Control** | Git, GitHub |
| **Development Environment** | VS Code |



## 📁 Project Structure:

```text
StudyVault-Personal-Learning-Assistant/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── ask.py
│   │   ├── conversations.py
│   │   ├── documents.py
│   │   └── search.py
│   │
│   └── services/
│       ├── __init__.py
│       ├── database.py
│       ├── embedding_service.py
│       ├── llm_service.py
│       ├── pdf_processor.py
│       ├── rag_service.py
│       ├── retrieval_service.py
│       ├── text_processor.py
│       └── vector_store.py
│
├── frontend/
│   ├── __init__.py
│   └── app.py
│
├── tests/
│   ├── test_api.py
│   ├── test_ask_api.py
│   ├── test_chunking.py
│   ├── test_conversation_api.py
│   ├── test_database.py
│   ├── test_database2.py
│   ├── test_document_api.py
│   ├── test_embeddings.py
│   ├── test_llm.py
│   ├── test_rag.py
│   ├── test_retrieval.py
│   └── test_vector_store.py
│
├── data/
│   ├── uploads/
│   └── vector_db/
│
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── pytest.ini
```

### 📂 Directory Overview:

| Directory / File | Purpose |
|---|---|
| `backend/` | Contains the FastAPI backend and core application logic |
| `backend/api/` | REST API endpoints for documents, search, questions, and conversations |
| `backend/services/` | Core services for RAG, embeddings, document processing, database, and vector storage |
| `frontend/` | Streamlit-based user interface |
| `tests/` | Automated tests for the application's major components |
| `data/uploads/` | Stores uploaded PDF documents locally |
| `data/vector_db/` | Stores the ChromaDB vector database locally |
| `.env.example` | Template for required environment variables |
| `.gitignore` | Specifies files and directories excluded from Git |
| `LICENSE` | Project license |
| `README.md` | Project documentation |
| `requirements.txt` | Python dependencies |
| `pytest.ini` | pytest configuration |


## 🔄 How It Works:
<p align="center">
<img width="1000" alt="ChatGPT Image Sep 17, 2026, 04_06_37 PM" src="https://github.com/user-attachments/assets/82f48ddf-6d2d-4b66-9891-8dcc99056830" />
</p>


## ⚙️ Installation:

Follow the steps below to set up StudyVault locally.

### 1. Clone the Repository:

```bash
git clone https://github.com/msns-1927/StudyVault-Personal-Learning-Assistant.git
cd StudyVault-Personal-Learning-Assistant
```
### 2. Create a Virtual Environment:

Windows:
```
python -m venv venv
venv\Scripts\activate
```
macOS / Linux:
```
python3 -m venv venv
source venv/bin/activate
```
### 3. Install Dependencies:
```
pip install -r requirements.txt
```
### 4. Configure Environment Variables:

Create a .env file in the project root directory:

```
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.5-flash-lite
CHROMA_COLLECTION=studyvault_documents
RELEVANCE_THRESHOLD=0.8
DEFAULT_TOP_K=5
MAX_TOP_K=20
MAX_UPLOAD_SIZE_MB=20
```
Replace `your_gemini_api_key_here` with your actual Gemini API key.

> Important: Never commit your `.env` file or expose your API key publicly. The `.env` file is excluded through `.gitignore`

### 5. Start the FastAPI Backend:

From the project root:

```
uvicorn backend.main:app --reload
```

The backend will be available at:

```
http://127.0.0.1:8000
```

FastAPI interactive API documentation:
```
http://127.0.0.1:8000/docs
```
### 6. Start the Streamlit Frontend:

Open a new terminal, activate the virtual environment, and run:
```
streamlit run frontend/app.py
```
The Streamlit application will open in your browser.

### 7. Run the Application:

Once both services are running:
```
Streamlit Frontend
        ↓
FastAPI Backend
        ↓
StudyVault RAG Pipeline
        ↓
ChromaDB + SQLite + Gemini
```
You can now upload your study materials, ask questions, view source citations, manage conversations, and use the available Study Modes.

### 📌 Prerequisites:
- Python 3.10+
- pip
- Git
- Gemini API key
- Internet connection for the Gemini API and initial embedding model download


