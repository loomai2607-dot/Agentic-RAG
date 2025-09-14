from fastapi import APIRouter, Request, UploadFile, File, HTTPException
from core.graph import build_rag_graph
#from db.mongo import get_mongo_collection
from fastapi import HTTPException
#from bson import ObjectId
#from transformers import AutoTokenizer, AutoModel
#import torch
from pinecone import Pinecone, ServerlessSpec
from PyPDF2 import PdfReader
import os
import uuid
import tiktoken  # For token counting
import re
from openai import OpenAI
import asyncio
from uuid import uuid4


router = APIRouter()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = "rag-index"
pc = Pinecone(api_key=PINECONE_API_KEY)

if PINECONE_INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=1024,  # must match OpenAI embedding dimensions
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
index = pc.Index(PINECONE_INDEX_NAME)

# OpenAI setup

BATCH_SIZE = 10

# Naive word-based chunker (≈1500 words ≈ 6000 tokens)
def chunk_text(text, max_words=1500):
    words = text.split()
    return [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]

# Embedding function using OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embed(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(
        input=texts,
        model="text-embedding-3-large",
        dimensions=1024
    )
    return [item.embedding for item in response.data]
@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        # Read file content
        if file.filename.endswith(".pdf"):
            content = ""
            reader = PdfReader(file.file)
            for page in reader.pages:
                content += page.extract_text() or ""
        elif file.filename.endswith(".txt"):
            content = await file.read()
            content = content.decode("utf-8")
        else:
            raise HTTPException(status_code=400, detail="Only .pdf and .txt files are supported")

        if not content.strip():
            raise HTTPException(status_code=400, detail="No readable content found in the file")

        chunks = chunk_text(content)
        if not chunks:
            raise HTTPException(status_code=400, detail="Document could not be chunked")

        chunk_index = 0
        for i in range(0, len(chunks), BATCH_SIZE):
            batch = chunks[i:i + BATCH_SIZE]
            batch = [c for c in batch if c.strip()]
            if not batch:
                continue

            embeddings = embed(batch)
            if len(embeddings) != len(batch):
                print(f"⚠️ Warning: OpenAI returned fewer embeddings than inputs: {len(embeddings)} vs {len(batch)}")
                min_len = min(len(batch), len(embeddings))
                batch = batch[:min_len]
                embeddings = embeddings[:min_len]

            vectors = []
            for j in range(len(batch)):
                chunk = batch[j]
                emb = embeddings[j]
                vectors.append({
                    "id": str(uuid4()),
                    "values": emb,
                    "metadata": {
                        "filename": file.filename,
                        "chunk_index": chunk_index,
                        "length": len(chunk),
                        "preview": chunk[:300]
                    }
                })
                chunk_index += 1

            index.upsert(vectors)
            await asyncio.sleep(0)

        return {"message": f"{chunk_index} chunks embedded and indexed successfully", "chunks": chunk_index}

    except Exception as e:
        print(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query")
async def query_route(req: Request):
    body = await req.json()
    query = body.get("query")

    graph = build_rag_graph()
    inputs = {"query": query, "context": "", "answer": ""}
    output = graph.invoke(inputs)

    trace_log = graph.get_graph().to_json()

    return {
        "answer": output["answer"],
        "trace_graph": {
            "nodes": [
                {"id": "Retriever", "label": "Retriever"},
                {"id": "RAG", "label": "RAG"}
            ],
            "edges": [
                {"source": "Retriever", "target": "RAG"}
            ]
        },
        "trace_log": output.get("trace", [])
    }


# @router.get("/trace/{id}")
# def get_trace(id: str):
#     collection = get_mongo_collection()
#     doc = collection.find_one({"_id": ObjectId(id)})
#     if not doc:
#         raise HTTPException(404, "Trace not found")
#     return {"trace": doc["trace"]}
