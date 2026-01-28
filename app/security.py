from fastapi import Request, HTTPException
import os

API_KEY = os.getenv("API_KEY")

async def verify_api_key(request: Request):
    api_key = request.headers.get("x-api-key")

    if not api_key:
        raise HTTPException(status_code=401, detail="API key missing")

    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

    return True
