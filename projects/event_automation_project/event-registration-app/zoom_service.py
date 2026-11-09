import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_zoom_access_token():
    account_id = os.getenv("ZOOM_ACCOUNT_ID")
    client_id = os.getenv("ZOOM_CLIENT_ID")
    client_secret = os.getenv("ZOOM_CLIENT_SECRET")

    url = "https://zoom.us/oauth/token"

    response = requests.post(
        url,
        params={
            "grant_type": "account_credentials",
            "account_id": account_id
        },
        auth=(client_id, client_secret)
    )

    response.raise_for_status()

    return response.json()["access_token"]

def create_zoom_meeting(event_name, event_date, event_time):
    access_token = get_zoom_access_token()

    url = "https://api.zoom.us/v2/users/me/meetings"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    meeting_data = {
        "topic": "Python Automation Workshop",
        "type": 2, # scheduled meetings
        "start_time":  f"{event_date}T{event_time}:00",
        "duration": 60,
        "timezone": "Europe/Stockholm"
    }

    response = requests.post(
        url,
        headers=headers,
        json=meeting_data
    )

    response.raise_for_status()

    return response.json()
