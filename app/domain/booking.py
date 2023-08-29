from pydantic import BaseModel

from typing import List
from datetime import date, time

class UpdateBooking(BaseModel):
    id : int
    date : date
    time : time

class Booking(BaseModel):
    user_id : int
    agent_id : int
    date : date
    time : time

class UserBooking(BaseModel):
    id : int
    user_id : int
    agent_id : int
    date : date
    time : time

    class Config:
        from_attributes = True

class Bookings(BaseModel):
    data : List[UserBooking] = []