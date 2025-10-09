import os
import sys
from importlib import reload
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from backend.app.db import base as db_base


@pytest.fixture(scope="session")
def app(tmp_path_factory):
    os.environ["NAME"] = "test-backend"
    os.environ["PORT"] = "8001"
    os.environ["SECRET_KEY"] = "test-secret"
    os.environ["ALGORITHM"] = "HS256"
    os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "5"
    os.environ["REFRESH_TOKEN_EXPIRE_MINUTES"] = "10"
    os.environ["ADMIN_NAME"] = "test-admin"
    os.environ["ADMIN_PASSWORD"] = "test-password"
    os.environ["PYTHONHASHSEED"] = "0"

    # if "backend.app.config" in sys.modules:
    #     reload(sys.modules["backend.app.config"])
    # else:
    #     import backend.app.config  # noqa: F401

    tmp_dir = tmp_path_factory.mktemp("db")
    db_path = Path(tmp_dir) / "test.db"
    test_db_url = f"sqlite:///{db_path}"

    engine = create_engine(
        test_db_url,
        connect_args={"check_same_thread": False},
    )
    db_base.engine = engine
    db_base.SessionLocal.configure(bind=engine)
    db_base.Base.metadata.create_all(bind=engine)

    from backend.app.main import create_app

    application = create_app()
    with TestClient(application) as client:
        yield client.app


@pytest.fixture()
def client(app):
    with TestClient(app) as client:
        yield client


@pytest.fixture()
def admin_credentials():
    return {
        "username": os.environ["ADMIN_NAME"],
        "password": os.environ["ADMIN_PASSWORD"],
    }
