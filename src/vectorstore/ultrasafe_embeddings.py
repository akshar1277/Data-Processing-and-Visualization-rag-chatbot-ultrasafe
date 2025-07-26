import requests
from typing import List
from langchain.embeddings.base import Embeddings


class UltraSafeAIEmbeddings(Embeddings):
    def __init__(
        self,
        api_key: str,
        api_url: str = "https://api.us.inc/usf/v1/embed/embeddings",
        model: str = "usf1-embed",
    ):
        self.api_key = api_key
        self.api_url = api_url
        self.model = model

    def embed_text(self, text: str) -> List[float]:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        payload = {"model": self.model, "input": text}
        response = requests.post(self.api_url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["result"]["data"][0]["embedding"]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_text(text) for text in texts]

    def embed_query(self, text: str) -> List[float]:
        return self.embed_text(text)
