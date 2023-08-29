from sqlalchemy import (
    Boolean, 
    Column, 
    ForeignKey, 
    Integer, 
    String, 
    Date,
    Time
)
from sqlalchemy.orm import relationship

from sqlalchemy_utils.types.choice import ChoiceType

import enum

from dependencies.database import Base

class User(Base):
    ROLES = [
        ('admin', 'Administrator'),
        ('client', 'Regular user')
    ]
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    role = Column(ChoiceType(ROLES), index=True)

    items = relationship("Booking", back_populates="user")

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    items = relationship("Booking", back_populates="agent")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    time = Column(Time, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), index=True)

    user = relationship("User", back_populates="items")
    agent = relationship("Agent", back_populates="items")