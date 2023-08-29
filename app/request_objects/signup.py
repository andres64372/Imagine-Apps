from pydantic import BaseModel
from enum import Enum

class Roles(str, Enum):
    ADMIN = "admin"
    CLIENT = "client"

class SignupRequest(BaseModel):
    email : str
    password : str
    first_name : str
    last_name : str
    role : Roles