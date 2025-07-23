import requests
from fastapi import HTTPException, Header

def verify_jwt(token: str):
    try:
        response = requests.get(
            "http://user-service:3000/api/user",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            return response.json()["user_id"]
        else:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=500, detail="Could not verify token")
