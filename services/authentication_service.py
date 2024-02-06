# stdlib
from datetime import datetime
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

# thirdparty
import jwt


# project
from settings import ACCESS_TOKEN_EXPIRY, JWT_SECRET, REFRESH_TOKEN_EXPIRY
from services.user_service import get_user_by_id
from db.db_setup import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(user_id: int):
    payload_access = {
        "user_id": user_id,
        "exp": datetime.utcnow() + ACCESS_TOKEN_EXPIRY,
    }

    access_token = jwt.encode(payload_access, JWT_SECRET)
    return access_token


def create_refresh_token(user_id: int):
    payload_refresh = {
        "user_id": user_id,
        "exp": datetime.utcnow() + REFRESH_TOKEN_EXPIRY,
    }

    access_token = jwt.encode(payload_refresh, JWT_SECRET)
    return access_token


async def get_current_user(
    session: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(token, JWT_SECRET, "HS256")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=409, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=409, detail="Invalid token")

    user = await get_user_by_id(session=session, user_id=payload["user_id"])

    if not user:
        raise HTTPException(status_code=409, detail="Invalid token")

    return user
