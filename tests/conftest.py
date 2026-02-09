import pytest
import sys, os
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import app
from db import Base
from dependencies import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush= False, 
    bind=engine
)

Base.metadata.create_all(bind=engine)

@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c