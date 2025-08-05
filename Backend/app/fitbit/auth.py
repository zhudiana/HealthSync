from fastapi import APIRouter, Request
from app.config import FITBIT_CLIENT_ID, FITBIT_CLIENT_SECRET, FITBIT_REDIRECT_URI
import requests
from urllib.parse import urlencode, quote
import base64
import secrets
import hashlib
import json
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.post("/fitbit/token")
def fitbit_token(data: dict):
    code = data["code"]
    code_verifier = data["code_verifier"]

    credentials = f"{FITBIT_CLIENT_ID}:{FITBIT_CLIENT_SECRET}"
    auth_header = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    token_url = "https://api.fitbit.com/oauth2/token"
    payload = {
        "client_id": FITBIT_CLIENT_ID,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": FITBIT_REDIRECT_URI,
        "code_verifier": code_verifier,
    }

    res = requests.post(token_url, headers=headers, data=payload)
    return res.json()

@router.get("/fitbit/mobile-callback")
def mobile_callback(code: str = None, state: str = None):
    # Redirect to your app using a deep link (e.g., healthsync://auth?code=xyz)
    return RedirectResponse(url=f"healthsync://auth?code={code}&state={state}")
