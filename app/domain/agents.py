from pydantic import BaseModel

from datetime import date, time
from typing import List

class Agent(BaseModel):
    id: int
    name : str

    class Config:
        from_attributes = True

class Agents(BaseModel):
    data : List[Agent] = []