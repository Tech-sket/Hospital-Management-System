from pathlib import Path
import json

from django.shortcuts import redirect
from django.http import JsonResponse

from google_auth_oauthlib.flow import Flow

# =========================
# PROJECT BASE DIRECTORY
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent
CREDENTIALS_FILE = BASE_DIR / "credentials.json"

# Google Calendar scope
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Your redirect URI (must match Google Cloud Console)
REDIRECT_URI = "http://127.0.0.1:8000/calendar/oauth2callback/"


# =========================
# STEP 1: START OAUTH FLOW
# =========================
def oauth2_start(request):
    flow = Flow.from_client_secrets_file(
        str(CREDENTIALS_FILE),
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )

    request.session["state"] = state

    return redirect(authorization_url)


# =========================
# STEP 2: OAUTH CALLBACK
# =========================
def oauth2_callback(request):
    state = request.session.get("state")

    flow = Flow.from_client_secrets_file(
        str(CREDENTIALS_FILE),
        scopes=SCOPES,
        state=state,
        redirect_uri=REDIRECT_URI
    )

    # Get token using response URL
    flow.fetch_token(authorization_response=request.build_absolute_uri())

    credentials = flow.credentials

    # IMPORTANT: Save these in DB (for now just return JSON)
    data = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret
    }

    return JsonResponse({
        "message": "Google Calendar connected successfully",
        "credentials": data
    })