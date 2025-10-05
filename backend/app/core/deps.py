from fastapi import Depends
from sqlalchemy.orm import Session

from backend.app.db.base import get_db
from backend.app.repository.user import UserRepository
from backend.app.service.user import UserService


def get_user_repository(db: Session = Depends(get_db)):
    return UserRepository(db)


def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    return UserService(user_repository)
