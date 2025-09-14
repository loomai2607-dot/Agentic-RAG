from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from app.agents.retriever import RetrieverAgent
from app.agents.rag_agent import RAGAgent

def setup_agents():
    retriever = RetrieverAgent()
    rag_agent = RAGAgent()

    group_chat = GroupChat(
        agents=[retriever, rag_agent],
        messages=[],
        max_round=3,
    )
    manager = GroupChatManager(groupchat=group_chat, name="Coordinator")
    
    user_proxy = UserProxyAgent(name="User", human_input_mode="NEVER", is_termination_msg=lambda x: x.get("content", "").endswith("FINAL"))
    return user_proxy, manager
