from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.orm import Session

from backend.app.core.security import decode_access_token
from backend.app.db.base import get_db
from backend.app.model.user import User
from backend.app.repository.auth import AuthRepository
from backend.app.repository.user import UserRepository
from backend.app.schemas.auth import TokenPayload
from backend.app.service.auth import AuthService
from backend.app.service.user import UserService
from backend.app.utils.enum import UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_user_repository(db: SessionDep) -> UserRepository:
    return UserRepository(db)


def get_user_service(user_repository: Annotated[UserRepository, Depends(get_user_repository)]) -> UserService:
    return UserService(user_repository)


def get_auth_repository(db: SessionDep) -> AuthRepository:
    return AuthRepository(db)


def get_auth_service(auth_repository: Annotated[AuthRepository, Depends(get_auth_repository)]) -> AuthService:
    return AuthService(auth_repository)


def get_current_user(db: SessionDep, token: TokenDep) -> User:
    payload_data = decode_access_token(token)
    try:
        payload = TokenPayload.model_validate(payload_data)
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        ) from exc

    if payload.type != "access":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token type",
        )

    user = db.get(User, payload.sub)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_user(current_user: CurrentUser) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


def get_current_active_admin(current_user: CurrentUser) -> User:
    role_value = current_user.role if isinstance(current_user.role, str) else current_user.role.value
    if role_value != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user
