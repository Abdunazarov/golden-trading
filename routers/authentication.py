# stdlib
import re

# thirdparty
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

# project
from db.schemas.authentication_schema import (
    UserCreateBody,
    RegisterResponse,
    LoginBody,
    LoginResponse,
)
from db.db_setup import get_session
from settings import EMAIL_PATTERN
from services.user_service import get_user_by_username, create_user
from services.authentication_service import create_access_token, create_refresh_token
from utils.send_email import send_email_async


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

    EMAIL_SUBJECT = "Тестовая отправка письма"
    EMAIL_BODY = (
        f"Здарова! Ты создал аккаунт на моем сайте. Твой аккаунт: {user.username}"
    )

    send_email_async(to=data.username.lower(), subject=EMAIL_SUBJECT, body=EMAIL_BODY)

    response = RegisterResponse(
        id=user_id,
        username=data.username,
        email=data.email,
        fio=data.fio,
        birthday=data.birthday,
        tags=data.tags,
    )

    return response


@authentication_router.post("/login", response_model=LoginResponse)
async def login(
    data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    """
    Authenticate an existing user
    """
    user = await get_user_by_username(session=session, username=data.username.lower())

    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")

    if not user.verify_password(password=data.password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    return {
        "access_token": create_access_token(user_id=user.id),
        "refresh_token": create_refresh_token(user_id=user.id),
    }
