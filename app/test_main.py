from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import jwt
from datetime import datetime, timedelta

from dependencies.database import Base, get_db
from dependencies.authorization import UserSession
from main import app
from conf import settings

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

session = UserSession(
    user=1, 
    role='admin',
    exp=datetime.utcnow() + timedelta(hours=1)
)

access_token = jwt.encode(
    session.model_dump(), 
    settings.SECRET, 
    algorithm="HS256"
)

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

def test_create_agent():
    response = client.post(
        "/agent",
        json={
            "name": "Agent 1"
        },
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    assert response.status_code == 201

def test_get_agent():
    response = client.get(
        "/agent",
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "data": [{
            "id": 1,
            "name": "Agent 1"
        }]
    }

def test_schedule():
    response = client.post(
        "/schedule",
        json={
            "agent_id": 1,
            "date": "2023-08-29",
            "time": "12:45:00"
        },
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    assert response.status_code == 201

def test_bad_schedule():
    response = client.post(
        "/schedule",
        json={
            "agent_id": 1,
            "date": "2023-08-29",
            "time": "12:40:00"
        },
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    assert response.status_code == 400

def test_update_booking():
    response = client.put(
        "/booking/1",
        json={
            "date": "2023-08-30",
            "time": "12:45:00"
        },
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    assert response.status_code == 200
    response = client.get(
        "/booking",
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "data": [{
            "id" : 1,
            "user_id" : 1,
            "agent_id" : 1,
            "date": "2023-08-30",
            "time": "12:45:00"
        }]
    }

def test_delete_booking():
    response = client.delete(
        "/booking/1",
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    assert response.status_code == 200