from fastapi import FastAPI
from pydantic import BaseModel

from database import Base, engine, SessionLocal
from models import Event as EventModel, Registration as RegistrationModel
from email_service import send_confirmation_email
from zoom_service import create_zoom_meeting


app = FastAPI()

Base.metadata.create_all(bind=engine) #This SQLAlchemy command creates the database tables defined by the  models.


class EventCreate(BaseModel):
    name: str
    date: str
    time: str
    description: str


@app.get("/")
def home():
    return {"message": "Event Registration App is working!"}

@app.post("/events")
def create_event(event: EventCreate):

    db = SessionLocal()

    # Create Zoom meeting
    zoom_meeting = create_zoom_meeting(  # calls the Zoom API.
        event.name,
        event.date,
        event.time
    )


    new_event = EventModel(
        name=event.name,
        date=event.date,
        time=event.time,
        description=event.description,
        zoom_link=zoom_meeting["join_url"]
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    db.close()

    return {
        "message": "Event created successfully",
        "event": {
            "id": new_event.id,
            "name": new_event.name,
            "date": new_event.date,
            "time": new_event.time,
            "description": new_event.description,
            "zoom_link": new_event.zoom_link
        }
    }




class RegistrationCreate(BaseModel):
    name: str
    email: str
    event_id: int

@app.post("/register")
def register(attendee: RegistrationCreate):

    db = SessionLocal()

    # Find the event
    event = db.query(EventModel).filter(
        EventModel.id == attendee.event_id
    ).first()

    if not event:
        db.close()
        return {"error": "Event not found"}

    new_registration = RegistrationModel(
        name=attendee.name,
        email=attendee.email,
        event_id=attendee.event_id
    )

    db.add(new_registration)
    db.commit()
    db.refresh(new_registration)

    send_confirmation_email(
        attendee.email,
        attendee.name,
        event.name,
        event.date,
        event.time,
        event.zoom_link
    )

    db.close()

    return {
        "message": "Registration successful",
        "registration": {
            "id": new_registration.id,
            "name": new_registration.name,
            "email": new_registration.email,
            "event_id": new_registration.event_id
        }
    }