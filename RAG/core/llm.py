from app.core.config import GROQ_API_KEY

def groq_llm_config(agent_name):
    return {
        "config_list": [{"api_key": GROQ_API_KEY, "base_url": "https://api.groq.com/openai/v1"}],
        "temperature": 0.3,
        "request_timeout": 60,
        "model": "mixtral-8x7b-32768",  # or llama3-70b
    }
