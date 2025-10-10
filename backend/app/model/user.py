from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from backend.app.db.base import Base


class User(Base):
    __tablename__ = 'USER'

    user_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    role = Column(String, nullable=False)
    refresh_tokens = relationship('RefreshToken', back_populates='user', cascade='all, delete-orphan')
