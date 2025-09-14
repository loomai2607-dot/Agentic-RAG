from pymongo import MongoClient
import os

def get_mongo_collection():
    client = MongoClient(os.getenv("MONGODB_URI"))
    db = client["agentic_rag"]
    return db["trace_logs"]
