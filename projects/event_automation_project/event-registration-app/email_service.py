import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()


def send_confirmation_email(to_email: str, name: str, event_name: str, event_date: str, event_time: str, zoom_link: str):
    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_PASSWORD")

    message = EmailMessage()

    message["Subject"] = "Event Registration Confirmed"
    message["From"] = sender_email
    message["To"] = to_email

    message.set_content(
        f"""Hi {name},

Your registration has been confirmed!

Event: {event_name}
Date: {event_date}
Time: {event_time}

Join the event:
{zoom_link}

Thank you for registering for our event.
See you there!

Best,
Event Registration By Laural
"""
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(message)


