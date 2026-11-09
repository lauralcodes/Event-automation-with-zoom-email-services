# Event Automation App

A Python API for creating online events, scheduling Zoom meetings, and registering attendees. Event and registration details are stored in SQLite, and attendees receive confirmation emails containing the event information and Zoom join link.

## Features

- Create events through a REST API
- Generate a scheduled Zoom meeting when an event is created
- Save events and attendee registrations in a local SQLite database
- Send registration confirmation emails with event details and the Zoom link
- Browse and test API endpoints using FastAPI's interactive documentation

## Tech Stack

- Python
- FastAPI and Pydantic
- SQLAlchemy
- SQLite
- Zoom API
- Gmail SMTP

## Requirements

- Python 3
- A Zoom Server-to-Server OAuth app with meeting permissions
- A Gmail account configured to send email through SMTP

## Setup

Open a terminal in the project directory and create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the dependencies:

```bash
pip install fastapi uvicorn sqlalchemy requests python-dotenv pydantic
```

Create a `.env` file in the project directory and add your credentials:

```env
ZOOM_ACCOUNT_ID=your_zoom_account_id
ZOOM_CLIENT_ID=your_zoom_client_id
ZOOM_CLIENT_SECRET=your_zoom_client_secret

EMAIL_ADDRESS=your_gmail_address
EMAIL_PASSWORD=your_gmail_app_password
```

For Gmail SMTP, use a Google App Password where required. Do not commit `.env` or put real credentials in your README.

## Run the App

Start the development server from the project directory:

```bash
uvicorn main:app --reload
```

The API will be available at:

- API root: http://127.0.0.1:8000/
- Interactive API documentation: http://127.0.0.1:8000/docs

The SQLite database, `events.db`, is created locally when the application initializes.

## API Endpoints

### Check the app

`GET /`

Returns a message confirming the application is running.

### Create an event

`POST /events`

Example request:

```json
{
  "name": "Python Automation Workshop",
  "date": "2026-12-10",
  "time": "14:30",
  "description": "A workshop about automating everyday tasks with Python."
}
```

The app creates a scheduled Zoom meeting and stores the event details, including the Zoom join link. The date should use `YYYY-MM-DD` format and the time should use `HH:MM` format.

### Register an attendee

`POST /register`

Example request:

```json
{
  "name": "Alex Morgan",
  "email": "alex@example.com",
  "event_id": 1
}
```

The app checks that the event exists, saves the attendee's registration, and sends a confirmation email with the event details and Zoom link.

## Data

The app uses SQLite and creates two tables:

- `events`: event name, date, time, description, and Zoom join link
- `registrations`: attendee name, email, and the associated event ID

## Current Limitations

- Zoom meetings are currently configured for 60 minutes and the `Europe/Stockholm` time zone.
- The Zoom meeting topic is currently hard-coded as `Python Automation Workshop`; it does not yet use the event name.
- The API does not currently include authentication or authorization.
- Email and Zoom credentials must be configured before the corresponding integrations can work.
