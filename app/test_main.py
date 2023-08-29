from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from dependencies.database import Base, get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_user():
    response = client.post(
        "/signup",
        json={
            "email": "andres64372@hotmail.com",
            "password": "medellin1998",
            "first_name": "Andres",
            "last_name": "Herrera",
            "role": "admin"
        },
    )
    assert response.status_code == 201

def test_login():
    response = client.post(
        "/login",
        json={
            "email": "andres64372@hotmail.com",
            "password": "medellin1998",
        },
    )
    assert response.status_code == 201