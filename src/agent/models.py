from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from src.utils.db import Base
from datetime import datetime

import uuid

class ChatHistoryModel(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user_table.id"))
    session_id = Column(String, default=lambda: str(uuid.uuid4()))
    session_title = Column(String, nullable=True)
    prompt = Column(String)    # What the user said
    response = Column(String)  # What the bot replied
    created_at = Column(DateTime, default=datetime.utcnow)
