import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    CHROMA_DB_PATH = os.getenv('CHROMA_DB_PATH', './chroma_db')
    COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'career-recommendations')
