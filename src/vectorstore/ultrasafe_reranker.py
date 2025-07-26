import requests
from typing import List, Dict


class UltraSafeAIReranker:
    """ 
    
    UltraSafeAIReranker class for reranking text based on a query using the UltraSafeAI API.
    This class provides a method to rerank a list of texts based on their relevance to a given query.

    """
    def __init__(
        self,
        api_key: str,
        api_url: str = "https://api.us.inc/usf/v1/embed/reranker",
        model: str = "usf1-rerank",
    ):
        self.api_key = api_key
        self.api_url = api_url
        self.model = model

    def rerank(self, query: str, texts: List[str]) -> List[int]:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        payload = {"model": self.model, "query": query, "texts": texts}

        response = requests.post(self.api_url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        # Sort by score descending, return list of indices
        sorted_indices = [
            item["index"]
            for item in sorted(
                data["result"]["data"], key=lambda x: x["score"], reverse=True
            )
        ]
        return sorted_indices
