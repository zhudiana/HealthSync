from fastapi import APIRouter, Request
from app.config import FITBIT_CLIENT_ID, FITBIT_CLIENT_SECRET, FITBIT_REDIRECT_URI
import requests
from urllib.parse import urlencode, quote
import base64
import secrets
import hashlib
import json

router = APIRouter()

# Store code verifiers temporarily (in production, use Redis or database)
code_verifiers = {}

def generate_code_verifier():
    return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')

def generate_code_challenge(verifier):
    digest = hashlib.sha256(verifier.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(digest).decode('utf-8').rstrip('=')

@router.get("/fitbit/login")
def fitbit_login():
    
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    
    # Store code verifier (use session ID or user ID as key in production)
    state = secrets.token_urlsafe(32)  # Anti-CSRF token
    code_verifiers[state] = code_verifier
    
    params = {
        "client_id": FITBIT_CLIENT_ID,
        "response_type": "code",
        "scope": "activity heartrate sleep profile",  
        "redirect_uri": FITBIT_REDIRECT_URI,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "state": state
    }
    
    query = urlencode(params, quote_via=quote)
    return {
        "url": f"https://www.fitbit.com/oauth2/authorize?{query}",
        "state": state  
    }

    
@router.get("/fitbit/callback")
def fitbit_callback(code: str, state: str = None):
    print(" Received code from Fitbit:", code)
    print(" Received state:", state)
    
    # Verify state and get code verifier
    if not state or state not in code_verifiers:
        return {"error": "Invalid state parameter - possible CSRF attack"}
    
    code_verifier = code_verifiers.pop(state)  # Remove after use
    
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
        "code": code,
        "code_verifier": code_verifier,  # Required for PKCE
        # Note: redirect_uri might be required depending on your app setup
        "redirect_uri": FITBIT_REDIRECT_URI,
    }
    
    token_url = "https://api.fitbit.com/oauth2/token"
    
    try:
        res = requests.post(token_url, headers=headers, data=data)
        res.raise_for_status()  # Raise exception for HTTP errors
        
        token_data = res.json()
        print("📥 Token response:", token_data)
        
        # Store tokens securely (use database in production)
        # token_data contains: access_token, refresh_token, expires_in, scope, user_id
        
        return token_data
        
    except requests.exceptions.HTTPError as e:
        print("❌ HTTP Error:", e)
        print("📦 Response status:", res.status_code)
        print("📦 Response text:", res.text)
        return {"error": f"HTTP {res.status_code}", "details": res.text}
    
    except Exception as e:
        print("❌ Error:", e)
        return {"error": "Failed to exchange code for token", "details": str(e)}