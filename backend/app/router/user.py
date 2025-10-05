from typing import Annotated

from fastapi import APIRouter, Depends, Form
from fastapi_utils.cbv import cbv

from backend.app.core.deps import get_user_service
from backend.app.service.user import UserService
from backend.app.schemas.user import UserCreate, UserUpdate

router = APIRouter(tags=["User API"], prefix="/api/users")


@cbv(router)
class UserRouter:
    def __init__(self, user_service: UserService = Depends(get_user_service)):
        self.user_service = user_service

    @router.post("/")
    def create_user(self, request: Annotated[UserCreate, Form()]):
        return self.user_service.create_user(request)

    @router.get("/")
    def get_all_users(self):
        return self.user_service.get_all_users()

    @router.get("/{user_id}")
    def get_user(self, user_id: int):
        return self.user_service.get_user(user_id)

    @router.patch("/{user_id}")
    def update_user(self, user_id: int, request: UserUpdate):
        return self.user_service.update_user(user_id, request)

    @router.patch("/{user_id}/activate")
    def activate_user(self, user_id: int):
        return self.user_service.activate_user(user_id)

    @router.delete("/{user_id}")
    def deactivate_user(self, user_id: int):
        return self.user_service.deactivate_user(user_id)
