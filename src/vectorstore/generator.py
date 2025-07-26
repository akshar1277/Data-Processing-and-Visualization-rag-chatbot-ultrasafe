import requests
import os
from typing import List
from langchain_core.documents import Document
from langfuse import observe
from src.config.langfuse import langfuse

ULTRASAFE_API_KEY = os.getenv("ULTRASAFE_API_KEY")


@observe(name="generate_answer_with_ultrasafeai")
def generate_answer_with_ultrasafeai(query: str, context_docs: List[Document]) -> str:
   

    context_text = "\n\n".join([doc.page_content for doc in context_docs])

    system_prompt = f"""
    You are an AI assistant restricted to answering **only** using the context provided below. You must not use external knowledge.

    - If the context doesn't contain an answer, respond exactly with: "I don't have relevant information to answer that question."
    - Do not guess or hallucinate. Do not rely on prior knowledge.
    - Keep your tone helpful and structured (bullet points if needed).

    Context:
    {context_text}
    """

    payload = {
        "model": "usf1-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
        "temperature": 0.1,
        "web_search": False,
        "stream": False,
        "max_tokens": 1000,
    }

    headers = {
        "Authorization": f"Bearer {ULTRASAFE_API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        "https://api.us.inc/usf/v1/hiring/chat/completions",
        json=payload,
        headers=headers,
    )

    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]
