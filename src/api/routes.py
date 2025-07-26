from fastapi import APIRouter, UploadFile, File, Request, HTTPException
import os
import shutil
import uuid

from src.vectorstore.ingestion_pipeline import process_and_store
from src.vectorstore.retriver import retrieve_relevant_chunks
from src.vectorstore.generator import generate_answer_with_ultrasafeai

from langfuse import observe
from src.config.langfuse import langfuse

from src.schemas.query import QueryRequest


router = APIRouter(tags=["Document"])


@observe(name="upload_doc")
@router.post("/upload")
async def upload_doc(request: Request, file: UploadFile = File(...)):
    user = request.state.user
    session_id = user.session_id
    if not session_id:
        raise HTTPException(status_code=400, detail="Missing session ID")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".pdf", ".doc", ".docx", ".txt"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    temp_filename = f"temp_{uuid.uuid4()}{ext}"
    with open(temp_filename, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        process_and_store(
            file_path=temp_filename, filename=file.filename, session_id=session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        os.remove(temp_filename)

    return {"message": "Document processed and stored successfully"}


@observe(name="query_docs")
@router.post("/query")
async def query_docs(request: Request, data: QueryRequest):
    user = request.state.user
    session_id = user.session_id

    if not session_id:
        raise HTTPException(status_code=400, detail="Missing session ID")

    query = data.query
    try:
        docs = retrieve_relevant_chunks(query, session_id=session_id)
        answer = generate_answer_with_ultrasafeai(query, docs)

        return {
            "query": query,
            "answer": answer,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
