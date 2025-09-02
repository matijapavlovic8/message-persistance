from fastapi import FastAPI
from pydantic import BaseModel
from chat import chat_with_ai

app = FastAPI(title="Chat AI Service")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    response = chat_with_ai(req.message)
    return ChatResponse(response=response)
