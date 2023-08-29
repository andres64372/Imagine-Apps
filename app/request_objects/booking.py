from pydantic import BaseModel

from datetime import date, time

class UpdateBookingRequest(BaseModel):
    date : date
    time : time