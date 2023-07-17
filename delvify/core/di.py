from datetime import datetime
from typing import Optional

from fastapi import HTTPException, Request
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from delvify.core import app_settings

# from .db import SessionLocal


def get_db() -> Session:
    try:
        db = Session()  # change to SessionLocal() if you are using a database
        return db
    finally:
        db.close()


def get_current_user_id(request: Request) -> Optional[int]:
    auth_header: str = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=403, detail="JWT token missing or incorrect type."
        )
    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(
            token,
            key=app_settings.SECRET_KEY.get_secret_value(),
            algorithms=[app_settings.TOKEN_ALGORITHM],
        )
        exp = payload.get("exp")
        if exp is not None:
            if datetime.utcnow() > datetime.fromtimestamp(exp):
                raise HTTPException(status_code=401, detail="Token has expired")

        user_id = payload.get("user_id")
        if user_id is not None:
            if isinstance(user_id, int):
                return user_id
            else:
                raise HTTPException(
                    status_code=401, detail="user_id in token should be an integer"
                )
        else:
            raise HTTPException(status_code=401, detail="No user_id found in the token")

    except JWTError:
        raise HTTPException(status_code=401, detail="JWT token could not be decoded.")
