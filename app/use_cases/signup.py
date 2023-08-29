from fastapi import HTTPException
from fastapi.responses import Response
import bcrypt

from request_objects.signup import SignupRequest
from repository.sql import DatabaseRepository

from models.models import User

class SignupUseCase:
    def __init__(self, database_repo: DatabaseRepository):
        self.__database_repo = database_repo

    def execute(self, request: SignupRequest):
        user = self.__database_repo.get_user_by_email(request.email)
        if user:
            raise HTTPException(
                401,
                'User already exists',
            )
        salt = bcrypt.gensalt()
        request.password = bcrypt.hashpw(
            request.password.encode('utf-8'), 
            salt
        ).decode('utf-8')
        user = User(**request.model_dump())
        self.__database_repo.create_user(user)
        return Response(status_code=201)
        
        