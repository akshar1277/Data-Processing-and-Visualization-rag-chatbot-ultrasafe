import os
import time
from pinecone import Pinecone, ServerlessSpec


def get_pinecone_index(
    api_key: str,
    index_name: str,
    dimension: int = 1024,
    region: str = "us-east-1",
    cloud: str = "aws",
):
    pc = Pinecone(api_key=api_key)

    if index_name not in [index_info["name"] for index_info in pc.list_indexes()]:
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(cloud=cloud, region=region),
        )
        while not pc.describe_index(index_name).status["ready"]:
            time.sleep(1)

    return pc.Index(index_name)
