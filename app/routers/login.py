from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from dependencies.database import get_db
from request_objects.login import LoginRequest
from repository.sql import DatabaseRepository
from use_cases.login import LooginUseCase

router = APIRouter()

@router.post(
    "/login",
    tags=["Autenticación"],
    summary="Create el token general de acceso",
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
) -> JSONResponse:
    database_repo = DatabaseRepository(db)
    use_case = LooginUseCase(database_repo)
    response = use_case.execute(request)
    return response