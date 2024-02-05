# stdlib
from typing import AsyncGenerator

# thirdparty
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# project
from settings import DATABASE_URL

Base = declarative_base()

async_engine = create_async_engine(
    DATABASE_URL
)
async_session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)



async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session.begin() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

