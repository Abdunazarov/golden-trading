# stdlib
from typing import Optional, List
from datetime import datetime

# thirdparty
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException

# project
from db.models.user_model import UserModel
from services.authentication_service import get_current_user
from db.db_setup import get_session
from services.user_service import get_all_users, get_users_by_filters
from db.schemas.user_schema import UsersResponse


users_router = APIRouter(prefix="/users", tags=["USERS"])


@users_router.get("", response_model=UsersResponse)
async def get_users(
    session: AsyncSession = Depends(get_session),
    user: UserModel = Depends(get_current_user),
):
    """
    Get users
    """
    users = await get_all_users(session=session)

    return {"results": users}


@users_router.get("/search", response_model=UsersResponse)
async def search_users(
    session: AsyncSession = Depends(get_session),
    user: UserModel = Depends(get_current_user),
    email: Optional[str] = None,
    username: Optional[str] = None,
    fio: Optional[str] = None,
    birthday: Optional[datetime] = None,
    tags: Optional[str] = None,
):
    """
    Get users by filters
    """
    tags = [tag for tag in tags.split(",")] if tags else None
    users = await get_users_by_filters(
        session=session,
        username=username,
        email=email,
        fio=fio,
        birthday=birthday,
        tag=tags,
    )

    return {"results": users}
