from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.database import get_db
from dependencies.authorization import user, UserSession
from repository.sql import DatabaseRepository
from use_cases.booking import GetBookingUseCase
from use_cases.booking import UpdateBookingUseCase
from use_cases.booking import DeleteBookingUseCase
from request_objects.booking import UpdateBookingRequest

router = APIRouter()

@router.get(
    "/booking",
    tags=["Reservas"],
    summary="Lista las reservas de cada usuario"
)
def booking(
    session: UserSession = Depends(user),
    db: Session = Depends(get_db)
):
    database_repo = DatabaseRepository(db, session)
    use_case = GetBookingUseCase(database_repo)
    response = use_case.execute()
    return response

@router.put(
    "/booking/{booking_id}",
    tags=["Reservas"],
    summary="Actualiza una reserva"
)
def update(
    booking_id: int,
    request: UpdateBookingRequest,
    session: UserSession = Depends(user),
    db: Session = Depends(get_db)
):
    database_repo = DatabaseRepository(db, session)
    use_case = UpdateBookingUseCase(database_repo)
    response = use_case.execute(booking_id, request)
    return response

@router.delete(
    "/booking/{booking_id}",
    tags=["Reservas"],
    summary="Elimina una reserva"
)
def delete(
    booking_id: int,
    session: UserSession = Depends(user),
    db: Session = Depends(get_db)
):
    database_repo = DatabaseRepository(db, session)
    use_case = DeleteBookingUseCase(database_repo)
    response = use_case.execute(booking_id)
    return response