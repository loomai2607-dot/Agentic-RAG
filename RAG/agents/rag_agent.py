from autogen import AssistantAgent
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class RAGAgent(AssistantAgent):
    def __init__(self):
        super().__init__(name="RAGAgent")

    def call_groq(self, prompt: str) -> str:
        import requests
        import os   

        api_key = os.getenv("GROQ_API_KEY")
        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }   

        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            json=payload,
            headers=headers
        )   

        try:
            res.raise_for_status()
            data = res.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            print("❌ Groq API Error:")
            print("Status Code:", res.status_code)
            print("Response:", res.text)
            raise RuntimeError("Groq call failed") from e   


    def execute(self, messages, sender, config):
        context = messages[-1]["content"]
        query = messages[0]["content"]
        prompt = f"""Use the following context to answer the question.
        
        ### CONTEXT
        {context}   
        ### QUESTION
        {query} 
        Respond clearly and accurately. FINAL"""
        output = self.call_groq(prompt)
        return {
            "name": self.name,
            "content": output
        }
    
    def call_with_context(self, query: str, context: str) -> str:
        prompt = f"""Use the following context to answer the question:

        ### CONTEXT
        {context}

        ### QUESTION
        {query}

        Respond clearly. FINAL
        """
        return self.call_groq(prompt)
