# stdlib
import json
from typing import List
from datetime import datetime

# thirdparty
from passlib.hash import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.dialects.postgresql import insert as pg_insert, JSON
from sqlalchemy import cast

# project
from db.models.user_model import UserModel
from db.schemas.authentication_schema import UserCreateBody


async def get_user_by_username(session: AsyncSession, username: str):
    query = select(UserModel).filter(UserModel.username == username)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def create_user(session: AsyncSession, user: UserCreateBody):
    user_config = {
        "fio": user.fio,
        "birthday": user.birthday.isoformat() if user.birthday else None,
        "tags": user.tags,
    }

    new_user = {
        "username": user.username.lower(),
        "email": user.email,
        "hashed_password": bcrypt.hash(user.password),
        "config": json.dumps(user_config),
    }

    stmt = (
        pg_insert(UserModel)
        .values(**new_user)
        .on_conflict_do_nothing(index_elements=["username"])
        .returning(UserModel.id)
    )
    result = await session.execute(stmt)
    session.commit()

    return result.scalar()


async def get_user_by_id(session: AsyncSession, user_id: int):
    query = select(UserModel).filter(UserModel.id == user_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()


async def get_all_users(session: AsyncSession, page: int, limit: int):
    result = await session.execute(select(UserModel))
    return result.scalars().all()


async def get_users_by_filters(
    session: AsyncSession,
    email: str,
    username: str,
    fio: str,
    birthday: datetime,
    tag: List[str],
):

    query = select(UserModel)

    if email:
        query = query.filter(UserModel.email == email)
    if username:
        query = query.filter(UserModel.username.ilike(f"%{username}%"))

    if fio:
        query = query.filter(UserModel.config["fio"].astext == fio)
    if birthday:
        query = query.filter(
            cast(UserModel.config["birthday"], JSON).astext == birthday.isoformat()
        )
    if tag:
        query = query.filter(UserModel.config["tags"].contains(cast(tag, JSON)))

    result = await session.execute(query)
    return result.scalars().all()
