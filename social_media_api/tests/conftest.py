import os

from typing import AsyncGenerator, Generator
import pytest

from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from social_media_api.database import engine, metadata, user_table

os.environ["ENV_STATE"] = "test"

from social_media_api.database import database  # noqa: E402

# Changed order so the "ENV_STATE" environment variable is set before loading the app
from social_media_api.main import app  # noqa: E402


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def client() -> Generator:
    yield TestClient(app)


@pytest.fixture(autouse=True, scope="function")
async def db() -> AsyncGenerator:
    await database.connect()
    metadata.create_all(engine)
    yield
    metadata.drop_all(engine)
    await database.disconnect()


@pytest.fixture
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=client.base_url) as ac:
        yield ac


@pytest.fixture
async def registered_user(async_client: AsyncClient) -> dict:
    user_details = {"email": "testregistered@example.com", "password": "1234"}
    await async_client.post("/register", json=user_details)
    query = user_table.select().where(user_table.c.email == user_details["email"])
    user = await database.fetch_one(query)
    user_details["id"] = user.id
    return user_details


@pytest.fixture
async def logged_in_token(async_client: AsyncClient, registered_user: dict) -> str:
    response = await async_client.post("/token", json=registered_user)
    return response.json()["access_token"]
