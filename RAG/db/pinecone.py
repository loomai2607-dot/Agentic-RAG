import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "rag-index")
PINECONE_REGION = os.getenv("PINECONE_ENVIRONMENT", "us-west-1")  # e.g., "us-west-2" or "gcp-starter"

pc = Pinecone(api_key=PINECONE_API_KEY)

# Create or get index
def get_or_create_index(dimension=1536):
    if PINECONE_INDEX_NAME not in pc.list_indexes().names():
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=dimension,
            metric='cosine',
            spec=ServerlessSpec(cloud="aws", region=PINECONE_REGION)
        )
    return pc.Index(PINECONE_INDEX_NAME)

# Add documents to index
def upsert_documents(index, documents):
    # Format: [(id, vector, {"text": "original text"})]
    index.upsert(vectors=documents)

# Query similar documents
def query_documents(index, vector, top_k=5):
    return index.query(vector=vector, top_k=top_k, include_metadata=True)
