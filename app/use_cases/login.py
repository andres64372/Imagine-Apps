from fastapi import HTTPException
from fastapi.responses import JSONResponse
import bcrypt
import jwt
from datetime import datetime, timedelta

from conf import settings
from dependencies.authorization import UserSession
from request_objects.login import LoginRequest
from repository.sql import DatabaseRepository

class LooginUseCase:
    def __init__(self, database_repo: DatabaseRepository):
        self.__database_repo = database_repo

    def execute(self, request: LoginRequest):
        user = self.__database_repo.get_user_by_email(request.email)
        if bcrypt.checkpw(
            request.password.encode('utf-8'), 
            user.password.encode('utf-8')
        ):
            session = UserSession(
                user=user.id, 
                role=user.role.code,
                exp=datetime.utcnow() + timedelta(hours=1)
            )
            access_token = jwt.encode(
                session.model_dump(), 
                settings.SECRET, 
                algorithm="HS256"
            )
            return JSONResponse(
                {'access_token': access_token}, 
                status_code=201
            )
        else:
            raise HTTPException(
                401,
                'Invalid credentials',
            )