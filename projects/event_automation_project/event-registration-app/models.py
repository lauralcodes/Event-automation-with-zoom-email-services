from sqlalchemy import Column, Integer, String
from database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    date = Column(String)
    time = Column(String)
    description = Column(String)
    zoom_link = Column(String)

class Registration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    event_id = Column(Integer)

