from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.app.db.base import Base


class RefreshToken(Base):
    __tablename__ = 'REFRESH_TOKEN'

    refresh_token_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey('USER.user_id'), nullable=False)
    jti = Column(String(255), nullable=False)
    family_id = Column(String(255), nullable=False)
    issued_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, nullable=False, default=False)

    user = relationship('User', back_populates='refresh_tokens')
