from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH")
MONGODB_URI = os.getenv("MONGODB_URI")
