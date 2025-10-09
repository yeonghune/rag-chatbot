from fastapi import APIRouter, Cookie, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.cbv import cbv

from backend.app.core.deps import CurrentUser, get_auth_service
from backend.app.schemas.auth import Token
from backend.app.schemas.user import UserOut
from backend.app.service.auth import AuthService

router = APIRouter(tags=["Auth API"], prefix="/api/auth")


@cbv(router)
class AuthRouter:
    def __init__(self, auth_service: AuthService = Depends(get_auth_service)):
        self.auth_service = auth_service

    @router.post("/token", response_model=Token)
    def login(self, response: Response, form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
        return self.auth_service.login(form_data, response)

    @router.post("/logout")
    def logout_current_session(self, response: Response, refresh_token: str | None = Cookie(None)) -> dict:
        self.auth_service.logout_current_session(refresh_token)
        response.delete_cookie(key="refresh_token", path="/")
        return {"success": True}

    @router.post("/logout/all")
    def logout_all_sessions(self, response: Response, refresh_token: str | None = Cookie(None)) -> dict:
        self.auth_service.logout_all_sessions(refresh_token)
        response.delete_cookie(key="refresh_token", path="/")
        return {"success": True}

    @router.post("/refresh", response_model=Token)
    def refresh_token(self, response: Response, refresh_token: str | None = Cookie(None)) -> Token:
        return self.auth_service.refresh_token(refresh_token, response)

    @router.get("/me", response_model=UserOut)
    def read_me(self, current_user: CurrentUser) -> UserOut:
        return UserOut.from_model(current_user)
