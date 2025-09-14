from chromadb import Client
from chromadb.config import Settings
import os

def get_chroma_client():
    return Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=os.getenv("CHROMA_DB_PATH", "./chroma_db")))

def create_collection(client, name="rag_collection"):
    if name in [c.name for c in client.list_collections()]:
        return client.get_collection(name)
    return client.create_collection(name=name)
