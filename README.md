# 📚 StudyVault-Personal-Learning-Assistant

<p align="center">
<img width="800" alt="ChatGPT Image Sep 16, 2026, 11_11_14 PM" src="https://github.com/user-attachments/assets/df6807d2-fb33-4d84-adb4-67e42f5bc141" />
</p>


## 🚀 Overview:

> StudyVault is a RAG-powered Personal Learning Assistant that helps students learn from their own study materials. Users can upload PDF documents, ask questions about their content, and receive clear, context-aware answers generated using Retrieval-Augmented Generation (RAG) with Gemini.

> The system processes uploaded documents through text extraction, cleaning, chunking, semantic embeddings, and vector storage using ChromaDB. When a user asks a question, StudyVault retrieves the most relevant content from the uploaded documents and provides an answer with source and page citations, helping users understand and verify the information.

> StudyVault also includes conversation history, document management, semantic search, relevance filtering, and multiple Study Modes such as Explain, Summary, Quiz, Flashcards, and Key Points, providing an interactive learning experience through a Streamlit frontend and FastAPI backend.


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
<img width="800" alt="ChatGPT Image Sep 17, 2026, 04_06_37 PM" src="https://github.com/user-attachments/assets/82f48ddf-6d2d-4b66-9891-8dcc99056830" />
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


## 🔌 API Endpoints:

StudyVault provides RESTful APIs through the FastAPI backend for document management, semantic search, RAG-based question answering, and conversation management.

### 📄 Document APIs:

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/documents/upload` | Upload and process a PDF document |
| `GET` | `/documents` | Retrieve all uploaded documents |
| `DELETE` | `/documents/{document_id}` | Delete a document and its associated data |

### 🔎 Search API:

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/search` | Perform semantic similarity search across uploaded documents |

**Request Example:**

```json
{
  "query": "What is machine learning?",
  "top_k": 5
  "conversation_id": null
}
```

### 🤖 Question Answering API:

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/ask` | Generate a RAG-based answer using relevant document context |

### 💬 Conversation APIs:

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/conversations` | Create a new conversation |
| `GET` | `/conversations` | Retrieve all conversations |
| `GET` | `/conversations/{conversation_id}` | Retrieve conversation details |
| `GET` | `/conversations/{conversation_id}/messages` | Retrieve messages from a conversation |
| `PATCH` | `/conversations/{conversation_id}` | Rename a conversation |
| `DELETE` | `/conversations/{conversation_id}` | Delete a conversation and its messages |

### ❤️ Health Check:

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Check whether the API is running |


### 📖 Interactive API Documentation:

FastAPI automatically provides interactive API documentation:

```
http://127.0.0.1:8000/docs
```

Alternative OpenAPI documentation:

```
http://127.0.0.1:8000/redoc
```


## 🧪 Testing:

StudyVault uses **pytest** to validate the functionality of its core components and APIs.

### Test Areas:

- **API Testing** — Validates FastAPI endpoints and API responses.
- **Document Processing** — Tests PDF text extraction, text cleaning, and chunking.
- **Embedding Service** — Validates embedding generation and vector dimensions.
- **Vector Store** — Tests ChromaDB storage, retrieval, document management, and deletion.
- **Semantic Retrieval** — Validates query embedding and relevant document retrieval.
- **RAG Service** — Tests context retrieval, prompt generation, relevance filtering, and answer generation.
- **LLM Service** — Validates Gemini integration and response generation.
- **Database** — Tests SQLite conversations, messages, and document metadata.
- **Conversation APIs** — Tests conversation creation, retrieval, renaming, and deletion.
- **Document APIs** — Tests document upload, validation, duplicate detection, and deletion.

### Running Tests:

Activate the virtual environment and run:

```bash
pytest
```

### Run Tests with Coverage:

```
pytest --cov=backend --cov-report=term-missing
```

### Test Structure:
```
tests/
├── test_api.py
├── test_ask_api.py
├── test_chunking.py
├── test_conversation_api.py
├── test_database.py
├── test_database2.py
├── test_document_api.py
├── test_embeddings.py
├── test_llm.py
├── test_rag.py
├── test_retrieval.py
└── test_vector_store.py
```

The test suite helps verify that the major StudyVault components work correctly and that changes to the application do not break existing functionality.



## ⚠️ Limitations:

- **PDF-Only Document Support** — The current document processing pipeline is designed to support PDF files. Other formats such as DOCX, TXT, and Markdown are not currently supported.

- **Local Data Storage** — Uploaded documents, ChromaDB vector data, and SQLite database records are stored locally on the system.

- **Single-User Application** — StudyVault currently does not include user authentication, authorization, or multi-user account management.

- **LLM Dependency** — Answer generation depends on the availability and configuration of the Gemini API.

- **Retrieval Dependency** — The quality of generated answers depends on the quality of document extraction, chunking, embeddings, and semantic retrieval.

- **Context-Based Answers** — StudyVault is designed to answer questions using information retrieved from the uploaded study materials. If relevant information is not available, the system may indicate that it could not find sufficient information.

- **Scanned PDF Limitations** — PDFs containing primarily scanned images may not provide extractable text unless OCR processing is added.

- **Local Resource Usage** — Embedding generation and vector database operations use the local machine's available CPU, memory, and storage resources.

- **No Production Deployment** — The current version is designed for local development and demonstration and has not been deployed as a production application.

- **No Advanced Authentication or Security Layer** — The current implementation does not provide production-grade authentication, role-based access control, or advanced security features.

- **Limited Conversation Intelligence** — Conversation history is maintained, but advanced query rewriting and sophisticated conversational retrieval techniques are not currently implemented.



## 🚀 Future Enhancements:

- 📄 **Multi-Format Document Support** — Extend document processing to support DOCX, TXT, and Markdown files in addition to PDFs.

- 🔐 **User Authentication & Authorization** — Add secure user accounts, authentication, and authorization for personalized learning environments.

- 👥 **Multi-User Support** — Enable multiple users to maintain separate documents, conversations, and learning history.

- 🔎 **Advanced Retrieval** — Improve retrieval using techniques such as hybrid search, reranking, and query expansion for better context selection.

- 🧠 **Advanced Conversational RAG** — Implement query rewriting and context-aware retrieval to improve responses to follow-up questions.

- 📝 **OCR Support** — Add Optical Character Recognition (OCR) to extract text from scanned and image-based documents.

- 📊 **Learning Analytics** — Track learning activity, frequently studied topics, quiz performance, and revision progress.

- 🎯 **Personalized Learning Paths** — Generate customized learning plans based on the user's study materials and learning progress.

- 🧩 **More Study Modes** — Expand the existing Study Modes with additional workflows such as practice tests, concept maps, and exam preparation.

- 🌐 **Production Deployment** — Deploy the application with scalable cloud infrastructure and persistent storage.

- 🔒 **Enhanced Security** — Add production-grade security measures including secure API handling, access controls, and data protection.

- ⚡ **Performance Optimization** — Improve document processing, embedding generation, retrieval speed, and overall application responsiveness.

- 💾 **Cloud Storage Integration** — Support cloud-based storage for documents, vector databases, and application data.

- 📱 **Responsive Interface** — Improve the user interface for a better experience across desktop, tablet, and mobile devices.


## Screenshots:

### 🖥️ StudyVault User Interface:

<p align="center">
<img width="900" alt="Screenshot 2026-09-16 230825" src="https://github.com/user-attachments/assets/197a2229-0c5e-47c6-8c75-bfe26ec711fa" />
</p>

### FastAPI Swagger Documentation:

<p align="center">
<img width="800" alt="Screenshot 2026-09-16 161124" src="https://github.com/user-attachments/assets/c04caacc-459d-4e74-8f66-2d0599ad9591" />
</p>




## 👨‍💻 Author

**Siva Narayana Muppidi**

- 💻 GitHub: [msns-1927](https://github.com/msns-1927)
- 🔗 LinkedIn: [Siva Narayana Muppidi](https://www.linkedin.com/in/siva-narayana-muppidi-413259230/)


## ⭐ If You Like StudyVault

If you found **StudyVault** useful or interesting, consider giving the repository a ⭐ **star** on GitHub. Your support and feedback are greatly appreciated!

> ⭐ **Like the project? Star the repository and help support its development!**

