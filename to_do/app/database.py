from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import func


DATABASE_URL = "postgresql+asyncpg://postgres:1111@localhost:5434/to_do_db"
engine = create_async_engine(DATABASE_URL)
Session = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(AsyncAttrs, DeclarativeBase):

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

async def get_db():
    session = Session()
    try:
        yield session
    finally:
        await session.close()
