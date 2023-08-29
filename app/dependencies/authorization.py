from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from enum import Enum
from datetime import datetime
import jwt

from conf import settings

class Roles(str, Enum):
    ADMIN = "admin"
    CLIENT = "client"

class UserSession(BaseModel):
    user : int
    role : Roles
    exp:  datetime

def validate_token(token: str):
    try:
        encoded = jwt.decode(
            token, 
            settings.SECRET, 
            algorithms=["HS256"]
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return UserSession.model_validate(encoded)

def user_admin(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    session = validate_token(token)
    if session.role != Roles.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User has not access to this resource",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return session

def user_client(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    session = validate_token(token)
    if session.role != Roles.CLIENT:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User has not access to this resource",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return session

def user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    return validate_token(token)