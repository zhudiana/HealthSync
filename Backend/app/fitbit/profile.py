from fastapi import APIRouter, Header, HTTPException
import requests

router = APIRouter()

@router.get("/fitbit/profile")
def get_fitbit_profile(authorization: str = Header(..., description="Bearer token")):
    """
    Get Fitbit user profile data.
    
    Args:
        authorization: Should be in format "Bearer <access_token>"
    """
    
    # Validate authorization header format
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=400, 
            detail="Authorization header must be in format 'Bearer <access_token>'"
        )
    
    headers = {
        "Authorization": authorization
    }
    
    try:
        res = requests.get("https://api.fitbit.com/1/user/-/profile.json", headers=headers)
        res.raise_for_status()  # Raise exception for HTTP errors
        
        profile_data = res.json()
        return profile_data
        
    except requests.exceptions.HTTPError as e:
        if res.status_code == 401:
            raise HTTPException(status_code=401, detail="Invalid or expired access token")
        elif res.status_code == 403:
            raise HTTPException(status_code=403, detail="Access forbidden - check scopes")
        else:
            raise HTTPException(
                status_code=res.status_code, 
                detail=f"Fitbit API error: {res.text}"
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch profile: {str(e)}")

@router.get("/fitbit/activities")
def get_fitbit_activities(authorization: str = Header(...), date: str = "today"):
    """
    Get Fitbit activity data for a specific date.
    
    Args:
        authorization: Bearer token
        date: Date in YYYY-MM-DD format or 'today'
    """
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=400, 
            detail="Authorization header must be in format 'Bearer <access_token>'"
        )
    
    headers = {
        "Authorization": authorization
    }
    
    try:
        res = requests.get(
            f"https://api.fitbit.com/1/user/-/activities/date/{date}.json", 
            headers=headers
        )
        res.raise_for_status()
        
        return res.json()
        
    except requests.exceptions.HTTPError as e:
        if res.status_code == 401:
            raise HTTPException(status_code=401, detail="Invalid or expired access token")
        elif res.status_code == 403:
            raise HTTPException(status_code=403, detail="Access forbidden - check scopes")
        else:
            raise HTTPException(
                status_code=res.status_code, 
                detail=f"Fitbit API error: {res.text}"
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch activities: {str(e)}")