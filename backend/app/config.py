import os

from pydantic_settings import BaseSettings, SettingsConfigDict

from backend import base_path

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(os.path.join(base_path, '.env')),
        env_ignore_empty=True,
    )

    NAME: str
    PORT: int
    SECRET_KEY: str
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ADMIN_NAME: str | None = None
    ADMIN_PASSWORD: str | None = None
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 14  # default two weeks

settings = Settings()