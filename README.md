# Data Processing and Visualization RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that allows users to upload documents (PDF, DOC, DOCX, TXT), processes them, and enables interactive Q&A over the uploaded content. The project features user authentication, document upload, and a conversational interface powered by Streamlit and FastAPI.

---

## Project Directory Structure

```
.
├── app.py                  # Streamlit frontend app
├── main.py                 # FastAPI backend entrypoint
├── requirements.txt        # Python dependencies
├── init_db.py              # Script to initialize the database
├── database.db             # SQLite database (auto-generated)
├── src/
│   ├── api/
│   │   ├── auth.py         # Auth endpoints (login, signup)
│   │   └── routes.py       # Upload and chatbot endpoints
│   ├── config/
│   │   ├── embedding.py    # Embedding configuration for UltraSafeAI
│   │   ├── pinecone.py     # Pinecone vector store configuration
│   │   ├── reranker.py     # Reranker configuration for UltraSafeAI
│   │   └── langfuse.py     # Langfuse configuration for observability
│   ├── db/
│   │   └── session.py      # Database session management
│   ├── middleware/
│   │   └── session_middleware.py # Middleware for session handling
│   ├── models/
│   │   └── user.py         # User model for authentication
│   ├── schemas/
│   │   ├── auth.py         # Request schemas for authentication
│   │   └── query.py        # Request schema for chatbot queries
│   ├── dependencies.py     # Dependency injection for FastAPI routes
│   └── vectorstore/
│       ├── generator.py         # Answer generation using UltraSafeAI
│       ├── ingestion_pipeline.py # Document ingestion and processing pipeline
│       ├── loader.py            # Document loader for various file types
│       ├── pinecone_client.py   # Pinecone client setup
│       ├── retriver.py          # Document retrieval logic
│       ├── ultrasafe_embeddings.py # Embedding generation using UltraSafeAI
│       ├── ultrasafe_reranker.py   # Reranking logic using UltraSafeAI
│       └── utils.py             # Utility functions for text processing
└── .gitignore                   # Git ignore rules
```

---

## Project Overview

This project implements a RAG-based chatbot system with the following features:

- **User Authentication:** Signup and login with secure password hashing.
- **Document Upload:** Upload PDF, DOC, DOCX, or TXT files for processing.
- **RAG Chatbot:** Ask questions about your uploaded documents and get context-aware answers.
- **Session Management:** Each user’s documents and chat sessions are isolated.
- **Frontend:** Streamlit app for easy interaction.
- **Backend:** FastAPI for API endpoints and document processing.

---

## API Endpoints

### 1. **Signup**
- **POST** `/auth/signup`
- **Body:** `{ "email": "user@example.com", "password": "yourpassword" }`
- **Response:** `{ "message": "User created", "user_id": <id> }`

### 2. **Login**
- **POST** `/auth/login`
- **Body:** `{ "email": "user@example.com", "password": "yourpassword" }`
- **Response:** `{ "message": "Logged in", "session_id": <session_id> }`
- **Note:** Sets a `session_id` cookie for authentication.

### 3. **Logout**
- **POST** `/auth/logout`
- **Headers:**
  - Cookie: `session_id=<session_id>`
- **Response:**
  ```json
  {
    "message": "Logged out successfully"
  }

### 4. **Upload Document**
- **POST** `/upload`
- **Form Data:** `file` (PDF, DOC, DOCX, or TXT)
- **Headers:** Cookie with `session_id`
- **Response:** `{ "message": "Document processed and stored successfully" }`

### 5. **Chatbot Query**
- **POST** `/query`
- **Body:** `{ "query": "Your question here" }`
- **Headers:** Cookie with `session_id`
- **Response:** `{ "query": "...", "answer": "..." }`


---

## Installation Guide

### 1. **Clone the Repository**
```bash
git clone <repo-url>
cd Data-Processing-and-Visualization-RAG-chatbot
```

### 2. **Create a Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. **Install Requirements**
```bash
pip install -r requirements.txt
```

### 4. **Initialize the Database**
```bash
python init_db.py
```

### 5. **Run the FastAPI Backend**
```bash
uvicorn main:app --reload
```
- The backend will be available at `http://localhost:8000`

### 6. **Run the Streamlit Frontend**
```bash
streamlit run app.py
```
- The frontend will be available at the URL shown in your terminal (usually `http://localhost:8501`).

---

## How to Use

### 1. **Sign Up / Log In**
- Open the Streamlit app in your browser.
- Use the authentication modal to sign up or log in.

### 2. **Upload a Document**
- Click the 📎 (paperclip) icon in the chat input area.
- Select a PDF, DOC, DOCX, or TXT file to upload.
- Wait for the upload confirmation.

### 3. **Chat with Your Document**
- Type your question in the chat input and press "Send".
- The chatbot will answer based on the content of your uploaded document.

### 4. **Session Management**
- Start new chat sessions or revisit previous ones from the sidebar.

### 5. **Logout**
- Use the "Logout" button in the sidebar to end your session.

---

## Notes

- Each user’s documents and chat sessions are private and isolated.
- Only supported file types can be uploaded (Pdf,docs,text).
- Make sure both backend and frontend are running for full functionality. 