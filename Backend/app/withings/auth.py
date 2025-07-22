from fastapi import APIRouter
from app.config import WITHINGS_CLIENT_ID, WITHINGS_REDIRECT_URI, WITHINGS_CLIENT_SECRET
from app.withings.utils import get_nonce, sign
import requests
from urllib.parse import urlencode

router = APIRouter()

@router.get("/withings/login")
def login_withings():
    params = {
        "response_type": "code",
        "client_id": WITHINGS_CLIENT_ID,
        "redirect_uri": WITHINGS_REDIRECT_URI,
        "scope": "user.metrics,user.activity",
        "state": "secure_random_state"
    }
    # query = "&".join(f"{k}={v}" for k, v in params.items())
    query = urlencode(params)
    return {"url": f"https://account.withings.com/oauth2_user/authorize2?{query}"}




@router.get("/withings/callback")
def withings_callback(code: str):
    nonce = get_nonce()
    print("nonce: ", nonce)
    params = {
        "action": "requesttoken",
        "client_id": WITHINGS_CLIENT_ID,
        "redirect_uri": WITHINGS_REDIRECT_URI,
        "grant_type": "authorization_code",
        "code": code,
        "nonce": nonce
    }
    signature = sign(params)
    

    base_string = "requesttoken,client_id_value,code_value,authorization_code,nonce_value,redirect_uri_value"
    params["signature"] = signature

    res = requests.post("https://wbsapi.withings.net/v2/oauth2", data=params)
    try:
        response_data = res.json()
        print("📥 Final response:", response_data)
        return response_data
    except Exception as e:
        print("❌ Failed to parse JSON:", e)
        print("📥 Raw response:", res.text)
        raise

