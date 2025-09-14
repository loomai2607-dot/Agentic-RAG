# graph.py
from langgraph.graph import StateGraph, END
from typing import TypedDict
from agents.retriever import RetrieverAgent
from agents.rag_agent import RAGAgent

class RAGState(TypedDict):
    query: str
    context: str
    answer: str
    trace: list  # Added trace for traceability

def build_rag_graph():
    rag_state = StateGraph(RAGState)

    retriever = RetrieverAgent()
    rag_agent = RAGAgent()

    def retrieve_node(state: RAGState) -> RAGState:
        docs = retriever.retrieve(state["query"])
        context = "\n".join(docs)
        trace_entry = {
            "node": "Retriever",
            "input": state["query"],
            "output": docs
        }
        return {
            **state,
            "context": context,
            "trace": state.get("trace", []) + [trace_entry]
        }

    def rag_node(state: RAGState) -> RAGState:
        answer = rag_agent.call_with_context(state["query"], state["context"])
        trace_entry = {
            "node": "RAG",
            "input": state["context"],
            "output": answer
        }
        return {
            **state,
            "answer": answer,
            "trace": state.get("trace", []) + [trace_entry]
        }

    rag_state.add_node("Retriever", retrieve_node)
    rag_state.add_node("RAG", rag_node)

    rag_state.set_entry_point("Retriever")
    rag_state.add_edge("Retriever", "RAG")
    rag_state.add_edge("RAG", END)

    return rag_state.compile()
