import uuid
from datetime import datetime, UTC

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
import requests
from config import API_BASE_URL, OPENAI_API_KEY, API_KEY

# Simple LLM instance
llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

def send_message_to_db(role: str, content: str):
    """Persist message in the main messages API."""
    payload = {
        "chat_id": str(uuid.uuid4()),
        "content": content,
        "role": role,
        "sent_at": datetime.now(UTC).isoformat()
    }
    headers = {"X-API-KEY": API_KEY}
    response = requests.post(f"{API_BASE_URL}/messages/", json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

def get_message_history():
    headers = {"X-API-KEY": API_KEY}
    response = requests.get(f"{API_BASE_URL}/messages/", headers=headers)
    response.raise_for_status()
    return response.json()

def chat_with_ai(user_input: str):
    send_message_to_db("human", user_input)
    history = get_message_history()
    messages = [
        HumanMessage(content=m["content"]) if m["role"]=="human" else AIMessage(content=m["content"])
        for m in history
    ]
    ai_msg = llm.invoke(messages + [HumanMessage(content=user_input)]).content.strip()
    send_message_to_db("ai", ai_msg)
    return ai_msg
