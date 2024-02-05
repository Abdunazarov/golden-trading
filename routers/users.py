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
from services.user_service import (
    get_all_users,
    get_users_by_filters,
    get_user_by_id,
    delete_user_by_id,
)
from db.schemas.user_schema import UsersResponse, SingleUserResponse


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


@users_router.post("/delete/{user_id}", response_model=SingleUserResponse)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    user: UserModel = Depends(get_current_user),
):
    """
    Get users
    """

    user = await get_user_by_id(session=session, user_id=user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")

    response = SingleUserResponse(
        id=user.id, username=user.username, email=user.email, config=user.config
    )

    await delete_user_by_id(session=session, user_id=user_id)

    return response


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

    for user in users:
        print(user.config, print(type(user.config)))

    return {"results": users}
