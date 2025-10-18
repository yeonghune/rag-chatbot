import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.app.db.base import Base


class Chat(Base):
    __tablename__ = 'CHAT'

    chat_id = Column(String(36), primary_key=True, nullable=False, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey('USER.user_id'), nullable=False)
    title = Column(String(30), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, nullable=False, default=False)

    user = relationship('User', back_populates='chats')
    messages = relationship('Message', back_populates='chat', cascade='all, delete-orphan')
