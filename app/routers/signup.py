from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from dependencies.database import get_db
from request_objects.signup import SignupRequest
from repository.sql import DatabaseRepository
from use_cases.signup import SignupUseCase

router = APIRouter()

@router.post(
    "/signup",
    tags=["Registro"],
    summary="Registra un usuario con un rol especifico"
)
def signup(
    request: SignupRequest,
    db: Session = Depends(get_db)
) -> JSONResponse:
    database_repo = DatabaseRepository(db)
    use_case = SignupUseCase(database_repo)
    response = use_case.execute(request)
    return response