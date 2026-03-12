import pytest
import asyncio
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from app.database import Base, get_db
from app.main import app

TEST_DB_URL = "postgresql+asyncpg://postgres:1111@localhost/test_todo_db"


@pytest_asyncio.fixture(scope='function')
async def async_db_engine():
    engine = create_async_engine(url=TEST_DB_URL,echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope='function')
async def async_db(async_db_engine):
    async_session = async_sessionmaker(
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
        bind=async_db_engine,
        class_=AsyncSession,
    )

    async with async_session() as  session:
        await session.begin()
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope='function', autouse=False)
async def async_client(async_db):
    async def override_db():
        yield async_db
    
    app.dependency_overrides[get_db] = override_db
    return AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://localhost'
    )


@pytest_asyncio.fixture(scope='function', autouse=False)
async def user_created(async_client):
    await async_client.post('/users/add/',
                            json={'email':'testuser@email.com',
                                'username': 'test_user',
                                'password': 'password'})
    

@pytest_asyncio.fixture(scope='function', autouse=False)
async def user_authenticated(async_client):
    await async_client.post('/users/add/',
                            json={'email':'testuser@email.com',
                                'username': 'test_user',
                                'password': 'password'})
    

    res = await async_client.post('/registration/login/',
                                  json={'email':'testuser@email.com',
                                         'password': 'password'})