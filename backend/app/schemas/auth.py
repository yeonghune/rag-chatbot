from pydantic import BaseModel

from backend.app.schemas.user import UserOut


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut


class TokenPayload(BaseModel):
    sub: int
    type: str
    jti: str | None = None
    family_id: str | None = None
