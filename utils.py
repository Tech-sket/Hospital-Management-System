import os

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


# Google Calendar OAuth Scope
SCOPES = [
    "https://www.googleapis.com/auth/calendar.events"
]


# -------------------------------------------------------
# OAuth Flow
# -------------------------------------------------------

def get_flow():
    """
    Create Google OAuth Flow
    """

    credentials_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "credentials.json"
    )

    flow = Flow.from_client_secrets_file(
        credentials_path,
        scopes=SCOPES,
        redirect_uri="http://localhost:8000/calendar/oauth2callback/"
    )

    return flow


# -------------------------------------------------------
# Get Google Login URL
# -------------------------------------------------------

def get_authorization_url():

    flow = get_flow()

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )

    return authorization_url, state


# -------------------------------------------------------
# Exchange Authorization Code
# -------------------------------------------------------

def exchange_code(code):

    flow = get_flow()

    flow.fetch_token(code=code)

    return flow.credentials


# -------------------------------------------------------
# Refresh Expired Token
# -------------------------------------------------------

def refresh_token_if_expired(credentials_dict):

    if not credentials_dict:
        return None

    creds = Credentials.from_authorized_user_info(
        credentials_dict,
        SCOPES
    )

    if creds.expired and creds.refresh_token:

        creds.refresh(Request())

        return {
            "token": creds.token,
            "refresh_token": creds.refresh_token,
            "token_uri": creds.token_uri,
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "scopes": creds.scopes,
        }

    return credentials_dict


# -------------------------------------------------------
# Create Calendar Event
# -------------------------------------------------------

def create_calendar_event(
    credentials_dict,
    summary,
    start_time,
    end_time,
    description=""
):

    if not credentials_dict:
        return None

    creds = Credentials.from_authorized_user_info(
        credentials_dict,
        SCOPES
    )

    service = build(
        "calendar",
        "v3",
        credentials=creds
    )

    event = {

        "summary": summary,

        "description": description,

        "start": {

            "dateTime": start_time.isoformat(),

            "timeZone": "Asia/Kolkata"

        },

        "end": {

            "dateTime": end_time.isoformat(),

            "timeZone": "Asia/Kolkata"

        }

    }

    created_event = service.events().insert(

        calendarId="primary",

        body=event

    ).execute()

    return created_event.get("htmlLink")