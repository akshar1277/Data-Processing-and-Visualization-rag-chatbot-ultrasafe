import os
from dotenv import load_dotenv

from src.vectorstore.ultrasafe_embeddings import UltraSafeAIEmbeddings


load_dotenv()

ULTRASAFE_API_KEY = os.getenv("ULTRASAFE_API_KEY")
ULTRASAFE_API_EMBEDDINGS_BASE = os.getenv(
    "ULTRASAFE_API_EMBEDDINGS_BASE", "https://api.us.inc/usf/v1/embed/embeddings"
)
ULTRASAFE_MODEL = os.getenv("ULTRASAFE_MODEL", "usf1-embed")


embedding_instance = UltraSafeAIEmbeddings(
    api_key=ULTRASAFE_API_KEY,
    api_url=ULTRASAFE_API_EMBEDDINGS_BASE,
    model=ULTRASAFE_MODEL,
)
