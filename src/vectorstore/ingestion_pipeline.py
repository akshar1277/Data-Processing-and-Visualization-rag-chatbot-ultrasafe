import os
import uuid
from datetime import datetime
from typing import List
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore

from src.vectorstore.loader import load_document
from src.vectorstore.utils import clean_text
from src.config.embedding import embedding_instance
from src.config.pinecone import index
from langfuse import observe
from src.config.langfuse import langfuse


load_dotenv()
BATCH_SIZE = 32
MAX_WORKERS = 4


def process_batch(batch_chunks, vector_store, session_id):
    """ 
    Process a batch of document chunks and store them in the vector store.

    """

    texts = [chunk.page_content for chunk in batch_chunks]
    metadatas = [chunk.metadata for chunk in batch_chunks]
    batch_ids = [chunk.metadata["chunk_id"] for chunk in batch_chunks]

    embedded_vectors = embedding_instance.embed_documents(texts)

    vector_store.index.upsert(
        vectors=[
            {"id": id_, "values": embedding, "metadata": {**metadata, "text": text}}
            for id_, embedding, text, metadata in zip(
                batch_ids, embedded_vectors, texts, metadatas
            )
        ],
        namespace=session_id,
    )
    return len(batch_chunks)


@observe(name="process_and_store")
def process_and_store(file_path: str, filename: str, session_id: str):

    """ 
    Process a document file, split it into chunks,modifying metadata and store them in the vector store.
    
    """

    docs: List[Document] = load_document(file_path)
    for doc in docs:
        doc.page_content = clean_text(doc.page_content)

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    for chunk in chunks:
        chunk.metadata.update(
            {
                "session_id": session_id,
                "chunk_id": str(uuid.uuid4()),
                "filename": filename,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

    vector_store = PineconeVectorStore(
        index=index, embedding=embedding_instance, namespace=session_id
    )

    batches = [chunks[i : i + BATCH_SIZE] for i in range(0, len(chunks), BATCH_SIZE)]

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        """ 
        Process document chunks in parallel using a thread pool.
        
        """
        futures = [
            executor.submit(process_batch, batch, vector_store, session_id)
            for batch in batches
        ]

        for i, future in enumerate(as_completed(futures), start=1):
            result = future.result()
            print(f"✅ Uploaded batch {i}: {result} chunks")

    print("✅ All chunks processed and uploaded.")
