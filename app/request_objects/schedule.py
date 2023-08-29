from pydantic import BaseModel

from datetime import date, time

class CreateScheduleRequest(BaseModel):
    agent_id : int
    date : date
    time : time