import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from backend.app.db.base import Base


class Message(Base):
    __tablename__ = 'MESSAGE'

    message_id = Column(String(36), primary_key=True, nullable=False, default=lambda: str(uuid.uuid4()))
    chat_id = Column(String(36), ForeignKey('CHAT.chat_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('USER.user_id'), nullable=False)
    sequence = Column(Integer, nullable=False)
    role = Column(String(10), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    chat = relationship('Chat', back_populates='messages')
    user = relationship('User', back_populates='messages')
