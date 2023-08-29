from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import Response
import json

from use_cases.schedule import get_slots
from repository.sql import DatabaseRepository
from domain.booking import UserBooking, Bookings
from request_objects.booking import UpdateBookingRequest

class GetBookingUseCase:
    def __init__(self, database_repo: DatabaseRepository):
        self.__database_repo = database_repo

    def execute(self):
        users = Bookings(data=[
            UserBooking.model_validate(booking)
            for booking in self.__database_repo.get_bookings()
        ])
        return JSONResponse(
            json.loads(users.model_dump_json())
        )

class UpdateBookingUseCase:
    def __init__(self, database_repo: DatabaseRepository):
        self.__database_repo = database_repo

    def execute(self, booking_id: int, request: UpdateBookingRequest):
        booking = self.__database_repo.get_booking_by_id(booking_id)
        if not booking:
            raise HTTPException(404)
        if booking.user_id == self.__database_repo.get_user_id():
            bookings = self.__database_repo.get_bookings_by_agent_and_date(
                booking.agent_id, 
                request.date
            )
            booked = [
                booking.time for booking in bookings 
            ]
            times = get_slots(booked)
            if request.time in times:
                self.__database_repo.update_booking(
                    booking_id, 
                    request.model_dump()
                )
                return Response(status_code=200)
            else:
                raise HTTPException(
                    401,
                    'Already scheduled',
                )
        else:
            raise HTTPException(
                401,
                'User is not authorized to delete this booking',
            )
    
class DeleteBookingUseCase:
    def __init__(self, database_repo: DatabaseRepository):
        self.__database_repo = database_repo

    def execute(self, id: int):
        booking = self.__database_repo.get_booking_by_id(id)
        if not booking:
            raise HTTPException(404)
        if booking.user_id == self.__database_repo.get_user_id():
            self.__database_repo.delete_booking(booking)
            return Response(status_code=200)
        else:
            raise HTTPException(
                401,
                'User is not authorized to delete this booking',
            )