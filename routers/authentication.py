# stdlib
import re

# thirdparty
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# project
from db.schemas.authentication_schema import UserCreateBody, RegisterResponse
from db.db_setup import get_session
from settings import EMAIL_PATTERN
from services.user_service import get_user_by_username, create_user


authentication_router = APIRouter(prefix="/auth", tags=["AUTHENTICATION"])


@authentication_router.post("/register", response_model=RegisterResponse)
async def register(data: UserCreateBody, session: AsyncSession = Depends(get_session)):
    """
    Register a new user
    """
    user = await get_user_by_username(session=session, username=data.username.lower())
    
    if user:
        raise HTTPException(status_code=400, detail="Username already taken")

    if data.email and not re.match(EMAIL_PATTERN, data.email):
        raise HTTPException(status_code=400, detail="Invalid email format")

    user_id = await create_user(session=session, user=data)

    response = RegisterResponse(
        id=user_id,
        username=data.username,
        email=data.email,
        fio=data.fio,
        birthday=data.birthday,
        tags=data.tags
    )

    return response
