import uuid
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from backend.app.config import settings
from backend.app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    verify_password,
)
from backend.app.model.refresh_token import RefreshToken
from backend.app.repository.auth import AuthRepository
from backend.app.schemas.auth import Token
from backend.app.schemas.user import UserOut


class AuthService:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository

    def login(self, form_data: OAuth2PasswordRequestForm, response: Response) -> Token:
        user = self.auth_repository.get_active_user_by_username(form_data.username)
        if user is None or not verify_password(form_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid ID or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        now = datetime.now(timezone.utc)
        access_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

        access_token = create_access_token(subject=str(user.user_id), expires_delta=access_expires)
        jti = str(uuid.uuid4())
        family_id = str(uuid.uuid4())
        refresh_token = create_refresh_token(
            subject=str(user.user_id),
            expires_delta=refresh_expires,
            jti=jti,
            family_id=family_id,
        )

        self.auth_repository.create_refresh_token(
            RefreshToken(
                user_id=user.user_id,
                jti=jti,
                family_id=family_id,
                issued_at=now,
                expires_at=now + refresh_expires,
                revoked=False,
            )
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            samesite="lax",
            path="/",
            max_age=int(refresh_expires.total_seconds()),
        )

        return Token(access_token=access_token, token_type="bearer", user=UserOut.from_model(user))

    def logout_current_session(self, refresh_token: str | None) -> bool:
        if refresh_token is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing")

        payload = decode_refresh_token(refresh_token)
        user_id = int(payload["sub"])
        family_id = payload["family_id"]

        tokens = self.auth_repository.find_tokens_by_session(user_id, family_id)
        for token in tokens:
            token.revoked = True
            self.auth_repository.update_refresh_token(token)
        return True

    def logout_all_sessions(self, refresh_token: str | None) -> bool:
        if refresh_token is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing")

        payload = decode_refresh_token(refresh_token)
        user_id = int(payload["sub"])

        tokens = self.auth_repository.find_tokens_by_user(user_id)
        for token in tokens:
            token.revoked = True
            self.auth_repository.update_refresh_token(token)
        return True

    def refresh_token(self, refresh_token: str | None, response: Response) -> Token:
        if refresh_token is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing")

        payload = decode_refresh_token(refresh_token)
        user_id = int(payload["sub"])
        jti = payload["jti"]
        family_id = payload["family_id"]

        if not self.auth_repository.is_refresh_token_valid(user_id, jti, family_id):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        stored_token = self.auth_repository.find_token(user_id, jti, family_id)
        if stored_token is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token not found")

        stored_token.revoked = True
        self.auth_repository.update_refresh_token(stored_token)

        now = datetime.now(timezone.utc)
        access_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

        access_token = create_access_token(subject=str(user_id), expires_delta=access_expires)
        new_jti = str(uuid.uuid4())
        new_refresh_token = create_refresh_token(
            subject=str(user_id),
            expires_delta=refresh_expires,
            jti=new_jti,
            family_id=family_id,
        )

        self.auth_repository.create_refresh_token(
            RefreshToken(
                user_id=user_id,
                jti=new_jti,
                family_id=family_id,
                issued_at=now,
                expires_at=now + refresh_expires,
                revoked=False,
            )
        )

        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
            samesite="lax",
            path="/",
            max_age=int(refresh_expires.total_seconds()),
        )

        user = self.auth_repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return Token(access_token=access_token, token_type="bearer", user=UserOut.from_model(user))
