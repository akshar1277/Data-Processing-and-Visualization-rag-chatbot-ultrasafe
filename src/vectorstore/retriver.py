from typing import List
from langchain_core.documents import Document
from langfuse import observe

from src.config.embedding import embedding_instance
from src.config.pinecone import index
from src.vectorstore.ultrasafe_reranker import UltraSafeAIReranker
from src.config.reranker import reranker_instance
from src.config.langfuse import langfuse


@observe(name="retrieve_relevant_chunks")
def retrieve_relevant_chunks(
    query: str, session_id: str, top_k: int = 5
) -> List[Document]:
    """ 
    
    Retrieve relevant document chunks based on the query using the Pinecone vector store and rerank them using UltraSafeAI.

    """

    embedded_query = embedding_instance.embed_query(query)

    search_results = index.query(
        vector=embedded_query,
        top_k=top_k,
        include_metadata=True,
        include_values=True,
        namespace=session_id,
    )

    documents = []
    texts = []
    for match in search_results["matches"]:

        text = match["metadata"].get("text", "")
        texts.append(text)
        documents.append(Document(page_content=text, metadata=match["metadata"]))

    try:
        ranked_indices = reranker_instance.rerank(query, texts)
        reranked_documents = [documents[i] for i in ranked_indices]
        return reranked_documents
    except Exception as e:
        print(f"[Reranking error] {e}. Returning unranked documents.")
        return documents
