from fastapi import Header, HTTPException, Security, status
from typing import Optional
import os

from app.config import API_KEY


def get_api_key(x_api_key: Optional[str] = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key"
        )
    return x_api_key