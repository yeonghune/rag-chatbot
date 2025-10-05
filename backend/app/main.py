from fastapi import FastAPI
import uvicorn

from backend.app.config import settings
from backend.app.db.base import Base, engine
from backend.app.router import user


def create_app() -> FastAPI:
    application = FastAPI(
        title=settings.NAME
    )

    Base.metadata.create_all(bind=engine)

    application.include_router(user.router)

    return application


app = create_app()

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=settings.PORT, reload=False)