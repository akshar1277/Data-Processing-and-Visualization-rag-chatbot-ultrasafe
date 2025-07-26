import os
from dotenv import load_dotenv
from src.vectorstore.pinecone_client import get_pinecone_index


load_dotenv()


PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX")
PINECONE_REGION = os.getenv("PINECONE_REGION", "us-east-1")
PINECONE_CLOUD = os.getenv("PINECONE_CLOUD", "aws")


index = get_pinecone_index(
    api_key=PINECONE_API_KEY,
    index_name=PINECONE_INDEX_NAME,
    region=PINECONE_REGION,
    cloud=PINECONE_CLOUD,
    dimension=1024,
)
