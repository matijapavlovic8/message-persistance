import uuid
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from .database import Base

class Message(Base):
    __tablename__ = "messages"

    message_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(UUID(as_uuid=True), nullable=False)
    content = Column(String, nullable=False)
    rating = Column(Boolean, nullable=True)
    sent_at = Column(DateTime, nullable=False)
    role = Column(String, nullable=False)
