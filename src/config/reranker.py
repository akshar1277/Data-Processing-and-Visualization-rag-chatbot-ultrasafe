from src.vectorstore.ultrasafe_reranker import UltraSafeAIReranker
import os
from dotenv import load_dotenv


load_dotenv()

ULTRASAFE_API_KEY = os.getenv("ULTRASAFE_API_KEY")  
reranker_instance = UltraSafeAIReranker(api_key=ULTRASAFE_API_KEY)
