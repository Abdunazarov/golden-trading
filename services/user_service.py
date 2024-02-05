# stdlib
import json

# thirdparty
from passlib.hash import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.dialects.postgresql import insert as pg_insert

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
        "tags": user.tags
    }

    new_user = {
        "username": user.username.lower(),
        "email": user.email,
        "hashed_password": bcrypt.hash(user.password),
        "config": json.dumps(user_config)
    }

    stmt = (
        pg_insert(UserModel)
        .values(**new_user)
        .on_conflict_do_nothing(index_elements=['username'])
        .returning(UserModel.id)
    )
    result = await session.execute(stmt)
    session.commit()

    return result.scalar()
