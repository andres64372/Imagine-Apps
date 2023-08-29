from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.database import get_db
from dependencies.authorization import user, user_admin, UserSession
from repository.sql import DatabaseRepository
from use_cases.agent import CreateAgentUseCase, GetAgentUseCase
from request_objects.agent import CreateAgentRequest

router = APIRouter()

@router.get(
    "/agent",
    tags=["Agentes"],
    summary="Lista los agentes disponibles para citas"
)
def users(
    session: UserSession = Depends(user),
    db: Session = Depends(get_db)
):
    database_repo = DatabaseRepository(db, session)
    use_case = GetAgentUseCase(database_repo)
    response = use_case.execute()
    return response

@router.post(
    "/agent",
    tags=["Agentes"],
    summary="Crea un nuevo agente (solo usuarios con rol de administrador)"
)
def agent(
    request: CreateAgentRequest,
    session: UserSession = Depends(user_admin),
    db: Session = Depends(get_db)
):
    database_repo = DatabaseRepository(db, session)
    use_case = CreateAgentUseCase(database_repo)
    response = use_case.execute(request)
    return response