from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from .main import app, get_db, Base

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

def test_create_user(client):
    response = client.post("/users/", json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"

def test_read_user(client):
    response = client.post("/users/", json={"username": "testuser2", "password": "testpassword2"})
    user_id = response.json()["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser2"
