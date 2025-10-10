from pydantic import BaseModel, Field, SecretStr, ConfigDict

from backend.app.model.user import User
from backend.app.core.security import get_password_hash
from backend.app.utils.enum import UserRole


class UserCreate(BaseModel):
    name: str = Field(alias="name")
    password: SecretStr = Field(alias="password")
    role: UserRole = Field(alias="userRole")

    model_config = ConfigDict(
        use_enum_values=True
    )

    def to_model(self) -> User:
        return User(
            name=self.name,
            password=get_password_hash(self.password.get_secret_value()),
            role=self.role
        )


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, alias="name")
    password: SecretStr | None = Field(default=None, alias="password")
    role: UserRole | None = Field(default=None, alias="userRole")

    model_config = ConfigDict(
        use_enum_values=True
    )

    def update_model(self, model: User) -> User:
        update_data = self.model_dump(by_alias=False, exclude_unset=True, exclude_none=True)
        for key, value in update_data.items():
            if key == 'password' and value is not None:
                value = get_password_hash(value.get_secret_value())
            setattr(model, key, value)
        return model


class UserOut(BaseModel):
    id: int = Field(alias="userId")
    name: str = Field(alias="name")
    role: UserRole = Field(alias="userRole")

    model_config = ConfigDict(
        use_enum_values=True
    )

    @classmethod
    def from_model(cls, model: User) -> "UserOut":
        return cls.model_validate(
            {
                "userId": model.user_id,
                "name": model.name,
                "userRole": model.role,
            },
            from_attributes=True,
        )
