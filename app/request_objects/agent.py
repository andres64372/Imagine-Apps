from pydantic import BaseModel

class CreateAgentRequest(BaseModel):
    name : str