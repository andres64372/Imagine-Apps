from pydantic import BaseModel

from datetime import date, time
from typing import List

class Schedule(BaseModel):
    date : date
    times : List[time] = []