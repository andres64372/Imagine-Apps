from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from dependencies.database import get_db
from dependencies.authorization import user, UserSession
from repository.sql import DatabaseRepository
from use_cases.schedule import AvailableScheduleUseCase
from use_cases.schedule import BookScheduleUseCase
from request_objects.schedule import CreateScheduleRequest

router = APIRouter()

@router.get(
    "/schedule",
    tags=["Reservas"],
    summary="Lista la disponiblidad de acuerdo a la fecha y el agente seleccionado"
)
def availability(
    agentId: int,
    date: date,
    session: UserSession = Depends(user),
    db: Session = Depends(get_db)
):
    database_repo = DatabaseRepository(db, session)
    use_case = AvailableScheduleUseCase(database_repo)
    response = use_case.execute(agentId, date)
    return response

@router.post(
    "/schedule",
    tags=["Reservas"],
    summary="Crea una reserva con fecha, hora y agente"
)
def create(
    request: CreateScheduleRequest,
    session: UserSession = Depends(user),
    db: Session = Depends(get_db)
):
    database_repo = DatabaseRepository(db, session)
    use_case = BookScheduleUseCase(database_repo)
    response = use_case.execute(request)
    return response