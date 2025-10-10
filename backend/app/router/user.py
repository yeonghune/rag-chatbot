from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from backend.app.core.deps import (
    get_current_active_admin,
    get_user_service,
)
from backend.app.model.user import User
from backend.app.schemas.user import UserCreate, UserUpdate, UserOut
from backend.app.service.user import UserService

router = APIRouter(tags=["User API"], prefix="/api/users")


@cbv(router)
class UserRouter:
    def __init__(self, user_service: UserService = Depends(get_user_service)):
        self.user_service = user_service

    @router.post("/", response_model=UserOut)
    def create_user(self, request: UserCreate, current_admin: User = Depends(get_current_active_admin)):
        return self.user_service.create_user(request)

    @router.get("/", response_model=list[UserOut])
    def get_all_users(self, current_admin: User = Depends(get_current_active_admin)):
        return self.user_service.get_all_users()

    @router.get("/{user_id}", response_model=UserOut)
    def get_user(self, user_id: int, current_admin: User = Depends(get_current_active_admin)):
        return self.user_service.get_user(user_id)

    @router.patch("/{user_id}", response_model=UserOut)
    def update_user(self, user_id: int, request: UserUpdate, current_admin: User = Depends(get_current_active_admin)):
        return self.user_service.update_user(user_id, request)

    @router.patch("/{user_id}/activate", response_model=bool)
    def activate_user(self, user_id: int, current_admin: User = Depends(get_current_active_admin)):
        return self.user_service.activate_user(user_id)

    @router.delete("/{user_id}", response_model=bool)
    def deactivate_user(self, user_id: int, current_admin: User = Depends(get_current_active_admin)):
        return self.user_service.deactivate_user(user_id)
