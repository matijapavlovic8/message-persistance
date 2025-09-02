from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class MessageBase(BaseModel):
    chat_id: UUID
    content: str
    rating: bool | None = None
    sent_at: datetime
    role: str

class MessageCreate(MessageBase):
    pass

class MessageUpdate(BaseModel):
    content: str | None = None
    rating: bool | None = None

class Message(MessageBase):
    message_id: UUID

    class Config:
        orm_mode = True
