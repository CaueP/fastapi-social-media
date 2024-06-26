import pytest
from random import randrange
from httpx import AsyncClient


async def register_user(async_client: AsyncClient, email: str, password: str):
    return await async_client.post(
        "/register",
        json={"email": email, "password": password},
    )


@pytest.mark.anyio
async def test_register_user(async_client: AsyncClient):
    email = f"test{randrange(999)}@example.net"
    response = await register_user(async_client, email, "1234")
    assert response.status_code == 201
    assert response.json()["email"] == email


@pytest.mark.anyio
async def test_register_user_already_exists(async_client: AsyncClient, registered_user: dict):
    response = await register_user(
        async_client,
        registered_user["email"],
        registered_user["password"],
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


@pytest.mark.anyio
async def test_login_user_not_exists(async_client: AsyncClient):
    response = await async_client.post(
        "/token",
        json={
            "email": "email@404.com",
            "password": "password",
        },
    )
    assert response.status_code == 401


@pytest.mark.anyio
async def test_login_user_exists(async_client: AsyncClient, registered_user: dict):
    response = await async_client.post(
        "/token",
        json={
            "email": registered_user["email"],
            "password": registered_user["password"],
        },
    )
    assert response.status_code == 200
