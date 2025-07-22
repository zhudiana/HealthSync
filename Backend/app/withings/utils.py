import time, hmac, hashlib
import requests
from app.config import WITHINGS_CLIENT_ID, WITHINGS_CLIENT_SECRET

def sign(params: dict) -> str:
    keys = sorted(k for k in params if k != "signature")  
    data = ",".join(str(params[k]) for k in keys)
    print("📦 Signing this string:", data)
    return hmac.new(WITHINGS_CLIENT_SECRET.encode(), data.encode(), hashlib.sha256).hexdigest()




def get_nonce() -> str:
    timestamp = int(time.time())
    params = {
        "action": "getnonce",
        "client_id": WITHINGS_CLIENT_ID,
        "timestamp": timestamp
    }
    signature = sign(params)
    print("🔑 Nonce request signature:", signature)
    params["signature"] = signature
    res = requests.post("https://wbsapi.withings.net/v2/signature", data=params)
    print("📡 Sent to Withings:", params)
    print("📥 Response status:", res.status_code)
    print("📥 Response body:", res.text)
   
    res.raise_for_status()
    return res.json()["body"]["nonce"]

def verify_signature(secret, data, signature):
    """Verify if a signature matches the expected HMAC"""
    computed = hmac.new(
        secret.encode('utf-8'),
        data.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return computed == signature