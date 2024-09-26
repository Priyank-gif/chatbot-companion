# models.py
from datetime import datetime

from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from typing_extensions import List


class UrlsModel(BaseModel):
    urls: List[str]


class QueryModel(BaseModel):
    query: str
    user_id: int
    chat_id: int
    chat_order: int


class TextModel(BaseModel):
    text: str = Field(..., example="Enter your text here to be vectorized")


class ChatMessageResponse(BaseModel):
    user_id: int
    chat_id: int
    chat_order: int
    message_type: str
    message: str


class ChatSessionResponse(BaseModel):
    user_id: int
    chat_id: int
    last_updated: datetime


Base = declarative_base()


class ChatSession(Base):
    __tablename__ = 'chat_sessions'

    user_id = Column(Integer, index=True)
    chat_id = Column(Integer, primary_key=True, index=True)
    last_updated = Column(TIMESTAMP, default=func.now())

    def __repr__(self):
        return f"<ChatSession(user_id={self.user_id}, chat_id={self.chat_id})>"


class ChatMessage(Base):
    __tablename__ = 'chat_messages'

    user_id = Column(Integer, index=True)
    chat_id = Column(Integer, index=True)
    message_type = Column(String, index=True)
    chat_order = Column(Integer, index=True)
    message = Column(Text)

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'chat_id', 'chat_order'),
        {},
    )

    def __repr__(self):
        return f"<ChatMessage(user_id={self.user_id}, chat_id={self.chat_id}, message_type={self.message_type}, chat_order={self.chat_order}, message='{self.message}')>"
