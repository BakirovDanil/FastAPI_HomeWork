from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from faststream import Depends
from typing import Annotated

DATABASE_URL = 'postgresql+asyncpg://danil:abobus@localhost/danil'

engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(bind = engine, class_= AsyncSession)
Base = declarative_base()

async def get_session():
    async with SessionLocal() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]
