from typing import List

from fastapi import HTTPException

from backend.app.repository.base import transactional
from backend.app.repository.user import UserRepository
from backend.app.schemas.user import UserCreate, UserUpdate, UserOut
from backend.app.model.user import User


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def _get_user(self, user_id: int) -> User:
        user = self.user_repo.get(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @transactional
    def create_user(self, request: UserCreate) -> UserOut:
        if self.user_repo.find_by_username(request.name):
            raise HTTPException(status_code=409, detail="User already exists")
        return UserOut.from_model(self.user_repo.add(request.to_model()))

    def get_all_users(self) -> List[UserOut]:
        users = self.user_repo.get_all()
        return [UserOut.from_model(user) for user in users] if users else []

    def get_user(self, user_id: int) -> UserOut:
        user = self._get_user(user_id)
        return UserOut.from_model(user)

    @transactional
    def update_user(self, user_id: int, request: UserUpdate) -> UserOut:
        user = self._get_user(user_id)
        user = request.update_model(user)

        return UserOut.from_model(self.user_repo.update(user))

    @transactional
    def activate_user(self, user_id: int) -> bool:
        user = self._get_user(user_id)
        return True if self.user_repo.activate(user) else False

    @transactional
    def deactivate_user(self, user_id: int) -> bool:
        user = self._get_user(user_id)
        return True if self.user_repo.deactivate(user) else False
