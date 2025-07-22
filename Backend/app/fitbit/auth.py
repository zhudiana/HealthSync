from fastapi import APIRouter, Request
from app.config import FITBIT_CLIENT_ID, FITBIT_CLIENT_SECRET, FITBIT_REDIRECT_URI
import requests
from urllib.parse import urlencode, quote
import base64

router = APIRouter()

# Step 1: Redirect user to Fitbit auth
@router.get("/fitbit/login")
def fitbit_login():
    params = {
        "client_id": FITBIT_CLIENT_ID,
        "response_type": "code",
        "scope": "activity heartrate sleep profile",  # customize scopes
        "redirect_uri": FITBIT_REDIRECT_URI,
        "expires_in": "604800"  # optional
    }
    query = urlencode(params, quote_via=quote)
    return {"url": f"https://www.fitbit.com/oauth2/authorize?{query}"}

# Step 2: Fitbit redirects back here with `code`
@router.get("/fitbit/callback")
def fitbit_callback(code: str):
    print("✅ Received code from Fitbit:", code)

    # Build the Basic Auth header (base64(client_id:client_secret))
    credentials = f"{FITBIT_CLIENT_ID}:{FITBIT_CLIENT_SECRET}"
    auth_header = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "client_id": FITBIT_CLIENT_ID,
        "grant_type": "authorization_code",
        "redirect_uri": FITBIT_REDIRECT_URI,
        "code": code
    }

    # Send POST request to Fitbit token endpoint
    token_url = "https://api.fitbit.com/oauth2/token"
    res = requests.post(token_url, headers=headers, data=data)

    try:
        token_data = res.json()
        print("📥 Token response:", token_data)
        return token_data
    except Exception as e:
        print("❌ Error parsing response:", e)
        print("📦 Raw response:", res.text)
        return {"error": "Failed to decode response"}
