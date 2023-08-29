from fastapi import HTTPException
from fastapi.responses import JSONResponse, Response
from typing import List
from datetime import date, time, timedelta
import json

from repository.sql import DatabaseRepository
from domain.schedule import Schedule
from domain.booking import Booking
from request_objects.schedule import CreateScheduleRequest
from models.models import Booking as BookingModel

def get_slots(booked: List[time]):
    start_time = time(8,0,0)
    end_time = time(17,0,0)
    current_time = start_time
    time_slot_duration = timedelta(minutes=15)
    available_slots = []
    while current_time <= end_time:
        if all(
            abs(current_time.hour - b.hour) > 0 or 
            abs(current_time.minute - b.minute) > 0
            for b in booked
        ):
            available_slots.append(current_time)
        hours, minutes = divmod((
            current_time.hour * 60 
            + current_time.minute 
            + time_slot_duration.seconds // 60
            ), 60)
        current_time = time(hours, minutes, 0)

    return [slot for slot in available_slots]

class AvailableScheduleUseCase:
    def __init__(self, database_repo: DatabaseRepository):
        self.__database_repo = database_repo

    def execute(self, agent_id: int, schedule_date: date):
        bookings = self.__database_repo.get_bookings_by_agent_and_date(agent_id, schedule_date)
        booked = [
            booking.time for booking in bookings 
        ]
        times = get_slots(booked)
        schedule = Schedule(date=schedule_date, times=times)
        return JSONResponse(
            json.loads(schedule.model_dump_json())
        )
        
class BookScheduleUseCase:
    def __init__(self, database_repo: DatabaseRepository):
        self.__database_repo = database_repo

    def execute(self, request: CreateScheduleRequest):
        if request.time.second != 0 or \
            request.time.minute % 15 != 0 or \
            request.time.hour < 8 or \
            request.time.hour >= 17:
            raise HTTPException(
                400,
                'Set time in 15 minutes interval from 08:00 to 17:00',
            )
        bookings = self.__database_repo.get_bookings_by_agent_and_date(
            request.agent_id, 
            request.date
        )
        booked = [
            booking.time for booking in bookings 
        ]
        times = get_slots(booked)
        if request.time in times:
            booking = Booking(
                user_id = self.__database_repo.get_user_id(),
                agent_id = request.agent_id,
                date = request.date,
                time = request.time
            )
            self.__database_repo.set_booking(BookingModel(**booking.model_dump()))
            return Response(status_code=201)
        else:
            raise HTTPException(
                401,
                'Already scheduled',
            )