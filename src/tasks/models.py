from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from src.utils.db import Base
from datetime import datetime

# This is my Modal form which our database table will be created 

# TaskModel is the table structre
class TaskModel(Base):

    __tablename__ = "user_tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    is_completed = Column(Boolean, default=False)
    priority = Column(String, default="medium")  # high, medium, low
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("user_table.id", ondelete="CASCADE"))