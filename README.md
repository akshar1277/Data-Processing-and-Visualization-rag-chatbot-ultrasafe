# Data Processing and Visualization RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that allows users to upload documents (PDF, DOC, DOCX, TXT), processes them, and enables interactive Q&A over the uploaded content. The project features user authentication, document upload, and a conversational interface powered by Streamlit and FastAPI.

---

## Documentation

For a detailed guide on this project, refer to the DeepWiki guide:

**[DeepWiki Guide: Data Processing and Visualization RAG Chatbot](https://deepwiki.com/akshar1277/Data-Processing-and-Visualization-rag-chatbot-ultrasafe/1-overview)**

---
## Postman Collection

To test the API endpoints, use the Postman collection:

**[Postman Collection: Data Processing and Visualization RAG Chatbot](https://documenter.getpostman.com/view/23504381/2sB34oDdP6)**

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

---

## System Architecture

The following diagram illustrates the architecture of the system, including the interaction between the frontend, backend, vector database, and external APIs:

![System Architecture](https://drive.google.com/file/d/1uI-g6R6WVILaATpijdt0myHpp3DB_NQJ/view?usp=sharing)

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

## Key Features

### 1. **Document Upload and Preprocessing**
- Users can upload documents in various formats, including **PDF, DOC, DOCX, and TXT**.
- During the upload process, **preprocessing techniques** such as text cleaning and chunking are applied to prepare the document for storage in the vector database.

### 2. **Vector Database Integration**
- The project uses **Pinecone** as the vector database to store document embeddings.
- Uploaded documents are split into smaller chunks, embedded using a custom embedding class, and stored in the vector database for efficient retrieval.

### 3. **Custom UltraSafe API Integration**
- Custom classes were created to interact with the **UltraSafeAI API** for embedding generation and reranking.
- The `UltraSafeAIEmbeddings` class handles the generation of embeddings for document chunks and queries.
- The `UltraSafeAIReranker` class is used to rerank retrieved results based on their relevance to the user query.

### 4. **Reranking for Enhanced Retrieval**
- During the retrieval process, the system applies **reranking** to ensure the most relevant document chunks are prioritized.
- This is achieved by leveraging the **UltraSafeAI reranking API**, which sorts the retrieved chunks based on their relevance scores.

### 5. **Interactive Q&A**
- Users can ask questions about their uploaded documents, and the chatbot provides **context-aware answers**.
- The chatbot strictly adheres to the provided document context, ensuring accurate and reliable responses.

### 6. **User Authentication and Session Management**
- Secure user authentication is implemented using **hashed passwords** and **session cookies**.
- Each user's documents and chat sessions are isolated, ensuring **privacy and security**.

### 7. **Langfuse Observability**
- The project integrates **Langfuse** for observability, providing detailed logs and tracing for chatbot interactions and performance monitoring.

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

## Sample `.env` File

Below is a sample `.env` file to configure the environment variables required for the project. Replace the placeholder values with your actual credentials and settings.

```properties
# Sample .env file
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENV=your-pinecone-environment
VECTOR_DIM=1536
INDEX_NAME=your-index-name
PINECONE_CLOUD=aws
PINECONE_REGION=your-region
PINECONE_INDEX=your-index-name
ULTRASAFE_API_KEY=your-ultrasafe-api-key
ULTRASAFE_API_EMBEDDINGS_BASE=https://api.your-domain.com/embed/embeddings
ULTRASAFE_MODEL=your-model-name
LANGFUSE_SECRET_KEY=your-langfuse-secret-key
LANGFUSE_PUBLIC_KEY=your-langfuse-public-key
LANGFUSE_HOST=https://your-langfuse-host.com
```

Make sure to keep your `.env` file private and never share it publicly to avoid exposing sensitive information.

---


## Langfuse Observability

Langfuse provides observability for the chatbot's interactions and performance. Below are two screenshots showcasing its functionality:

### Screenshot 1: **Chatbot Dashboard Logs**

![Langfuse Dashboard Logs](https://drive.google.com/uc?export=view&id=12302blWCT7L6UTGMZ_G1y-KSLtox7pHX)

### Screenshot 2: **Langfuse Tracing**
![Langfuse Tracing](https://drive.google.com/uc?export=view&id=1sq-sVwf4IEd74AYRQOSGZ7Kuu_PrqKz9)

## Notes

- Each user’s documents and chat sessions are private and isolated.
- Only supported file types can be uploaded (Pdf,docs,text).
- Make sure both backend and frontend are running for full functionality. 