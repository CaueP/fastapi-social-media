from typing import AsyncGenerator, Generator
import pytest

from fastapi.testclient import TestClient
from httpx import AsyncClient

from social_media_api.main import app
from social_media_api.routers.post import post_table, comment_table


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def client() -> Generator:
    yield TestClient(app)


@pytest.fixture(autouse=True)
def db() -> Generator:
    post_table.clear()
    comment_table.clear()
    yield

@pytest.fixture
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        yield ac
