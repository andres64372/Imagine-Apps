from typing import List
from sqlalchemy.orm import Session
from datetime import date

from dependencies.authorization import UserSession

from models.models import User, Agent, Booking

class DatabaseRepository:
    def __init__(self, db: Session, user: UserSession = None):
        self.__db = db
        self.__user = user

    def get_user_id(self):
        return self.__user.user

    def get_user_by_email(self, email) -> User:
        return self.__db.query(User) \
            .filter(User.email == email) \
            .first()
    
    def get_agents(self) -> List[Agent]:
        return self.__db.query(Agent).all()
    
    def get_booking_by_id(self, id: int) -> Booking:
        return self.__db.query(Booking) \
            .filter(Booking.id == id) \
            .first()
    
    def get_bookings(self) -> List[Booking]:
        # return self.__db.query(Booking) \
        #     .filter(Booking.user_id == self.get_user_id()) \
        #     .all()
        return self.__db.query(Booking).all()
    
    def get_bookings_by_agent_and_date(
            self, 
            agent_id: int, 
            date: date
        ) -> List[Booking]:
        return self.__db.query(Booking) \
            .filter(
                Booking.agent_id == agent_id, 
                Booking.date == date
            ).all()
    
    def set_booking(self, booking: Booking):
        self.__db.add(booking)
        self.__db.commit()

    def update_booking(self, booking_id: int, data: dict):
        self.__db.query(Booking).filter(Booking.id == booking_id) \
            .update(data, synchronize_session=False)
        self.__db.commit()
    
    def delete_booking(self, booking: Booking):
        self.__db.delete(booking)
        self.__db.commit()
    
    def create_user(self, user: User):
        self.__db.add(user)
        self.__db.commit()

    def create_agent(self, agent: Agent):
        self.__db.add(agent)
        self.__db.commit()