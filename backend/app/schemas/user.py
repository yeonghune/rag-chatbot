from pydantic import BaseModel, Field, SecretStr, ConfigDict

from backend.app.utils.enum import UserRole
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
            password=self.password.get_secret_value(),
            role=self.role
        )


class UserUpdate(BaseModel):
    name: str = Field(alias="name")
    password: str = Field(alias="password")
    role: UserRole = Field(alias="userRole")

    model_config = ConfigDict(
        use_enum_values=True
    )

    def update_model(self, model: User) -> User:
        update_data = self.model_dump(by_alias=False, exclude_unset=True)
        for key, value in update_data.items():
            value = get_password_hash(value.get_secret_value()) if key == 'password' else value
            setattr(model, key, value)
        return model


class UserOut(BaseModel):
    name: str = Field(alias="name")
    role: UserRole = Field(alias="userRole")

    model_config = ConfigDict(
        use_enum_values=True
    )

    def from_model(self):
        return User(
            name=self.name,
            role=self.role
        )
