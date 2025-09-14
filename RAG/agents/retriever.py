from autogen import AssistantAgent
from db.pinecone import get_or_create_index, query_documents
from openai import OpenAI
import os

class RetrieverAgent(AssistantAgent):
    def __init__(self):
        super().__init__(name="RetrieverAgent")
        self.index = get_or_create_index(dimension=1024)  # Must match Pinecone index
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def embed_query(self, query: str) -> list[float]:
        response = self.client.embeddings.create(
            model="text-embedding-3-large",
            input=[query],
            dimensions=1024
        )
        return response.data[0].embedding

    def retrieve(self, query: str, top_k: int = 5):
        embedded_query = self.embed_query(query)
        results = query_documents(self.index, embedded_query, top_k=top_k)
        docs = [match.metadata.get("text", "") for match in results["matches"] if "text" in match.metadata]
        return docs

    def execute(self, messages, sender, config):
        query = messages[-1]["content"]
        docs = self.retrieve(query)
        return {
            "name": self.name,
            "content": "\n".join(docs) + "\nFINAL"
        }
