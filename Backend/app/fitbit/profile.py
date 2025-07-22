from fastapi import APIRouter, Header
import requests

router = APIRouter()

@router.get("/fitbit/profile")
def get_fitbit_profile(authorization: str = Header(...)):
    headers = {
        "Authorization": authorization  # Pass "Bearer {access_token}" from frontend
    }

    res = requests.get("https://api.fitbit.com/1/user/-/profile.json", headers=headers)

    try:
        return res.json()
    except:
        return {"error": "Failed to parse response", "raw": res.text}
