import os

from typing import AsyncGenerator, Generator
import pytest

from fastapi.testclient import TestClient
from httpx import AsyncClient
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
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        yield ac
