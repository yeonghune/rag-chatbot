from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from backend.app.model.refresh_token import RefreshToken
from backend.app.model.user import User


class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.name == username).first()

    def get_active_user_by_username(self, username: str) -> Optional[User]:
        return (
            self.db.query(User)
            .filter(User.name == username, User.is_active.is_(True))
            .first()
        )

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.get(User, user_id)

    def create_refresh_token(self, token: RefreshToken) -> RefreshToken:
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        return token

    def find_tokens_by_session(self, user_id: int, family_id: str) -> list[RefreshToken]:
        return (
            self.db.query(RefreshToken)
            .filter(RefreshToken.user_id == user_id, RefreshToken.family_id == family_id, RefreshToken.revoked.is_(False))
            .all()
        )

    def find_tokens_by_user(self, user_id: int) -> list[RefreshToken]:
        return (
            self.db.query(RefreshToken)
            .filter(RefreshToken.user_id == user_id, RefreshToken.revoked.is_(False))
            .all()
        )

    def find_token(self, user_id: int, jti: str, family_id: str) -> Optional[RefreshToken]:
        return (
            self.db.query(RefreshToken)
            .filter(
                RefreshToken.user_id == user_id,
                RefreshToken.jti == jti,
                RefreshToken.family_id == family_id,
            )
            .first()
        )

    def is_refresh_token_valid(self, user_id: int, jti: str, family_id: str) -> bool:
        token = self.find_token(user_id, jti, family_id)
        if token is None or token.revoked:
            return False
        current_time = (
            datetime.now(token.expires_at.tzinfo)
            if token.expires_at.tzinfo
            else datetime.utcnow()
        )
        if token.expires_at <= current_time:
            return False
        return True

    def update_refresh_token(self, token: RefreshToken) -> RefreshToken:
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        return token
