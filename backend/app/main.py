from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from backend.app.config import settings
from backend.app.core.security import get_password_hash
from backend.app.db.base import Base, SessionLocal, engine
from backend.app.model.user import User
from backend.app.router import auth, user
from backend.app.utils.enum import UserRole


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)

    if settings.ADMIN_NAME and settings.ADMIN_PASSWORD:
        with SessionLocal() as session:
            existing_admin = session.query(User).filter(User.name == settings.ADMIN_NAME).first()
            if existing_admin is None:
                admin_user = User(
                    name=settings.ADMIN_NAME,
                    password=get_password_hash(settings.ADMIN_PASSWORD),
                    role=UserRole.ADMIN.value,
                    is_active=True,
                )
                session.add(admin_user)
                session.commit()

    yield


def create_app() -> FastAPI:
    application = FastAPI(title=settings.NAME, lifespan=lifespan)
    application.include_router(auth.router)
    application.include_router(user.router)
    return application


app = create_app()

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=settings.PORT, reload=False)
