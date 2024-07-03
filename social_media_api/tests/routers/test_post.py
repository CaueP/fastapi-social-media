from fastapi import security
import pytest
from httpx import AsyncClient
from social_media_api.security import create_access_token


async def create_post(body: str, async_client: AsyncClient, logged_in_token: str) -> dict:
    response = await async_client.post(
        "/post",
        json={"body": body},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    return response.json()


async def create_comment(
    body: str,
    post_id: int,
    async_client: AsyncClient,
    logged_in_token: str,
) -> dict:
    response = await async_client.post(
        "/comment",
        json={"body": body, "post_id": post_id},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    return response.json()


@pytest.fixture
async def created_post(async_client: AsyncClient, logged_in_token: str) -> dict:
    return await create_post("Test post", async_client, logged_in_token)


@pytest.fixture
async def created_comment(
    async_client: AsyncClient, created_post: dict, logged_in_token: str
) -> dict:
    return await create_comment("Test post", created_post["id"], async_client, logged_in_token)


@pytest.mark.anyio
async def test_create_post(async_client: AsyncClient, logged_in_token: str) -> None:
    body = "Test post"
    response = await async_client.post(
        "/post",
        json={"body": body},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )

    assert response.status_code == 201
    assert {"id": 1, "body": body}.items() == response.json().items()


@pytest.mark.anyio
async def test_create_post_expired_token(async_client: AsyncClient, registered_user: dict, mocker):
    mocker.patch(
        "social_media_api.security.access_token_expire_minutes",
        return_value=-1,
    )
    token = create_access_token(registered_user["email"])
    response = await async_client.post(
        "/post",
        json={"body": "Test post"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
    assert "Token has expired" in response.json()["detail"]


@pytest.mark.anyio
async def test_create_post_missing_data(async_client: AsyncClient, logged_in_token: str) -> None:
    response = await async_client.post(
        "/post",
        json={},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )

    assert response.status_code == 422


@pytest.mark.anyio
async def test_get_all_posts(async_client: AsyncClient, created_post: dict) -> None:
    response = await async_client.get("/post")

    assert response.status_code == 200
    assert response.json() == [created_post]


@pytest.mark.anyio
async def test_create_comment(
    async_client: AsyncClient, created_post, logged_in_token: str
) -> None:
    body = "Test comment"
    response = await async_client.post(
        "/comment",
        json={"body": body, "post_id": created_post["id"]},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    assert response.status_code == 201
    assert {
        "id": 1,
        "body": body,
        "post_id": created_post["id"],
    }.items() <= response.json().items()


@pytest.mark.anyio
async def test_create_comment_expired_token(
    async_client: AsyncClient, created_post, registered_user: dict, mocker
):
    mocker.patch(
        "social_media_api.security.access_token_expire_minutes",
        return_value=-1,
    )
    token = create_access_token(registered_user["email"])

    body = "Test comment"
    response = await async_client.post(
        "/comment",
        json={"body": body, "post_id": created_post["id"]},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
    assert "Token has expired" in response.json()["detail"]


@pytest.mark.anyio
async def test_get_comments_on_post(
    async_client: AsyncClient, created_post: dict, created_comment: dict
) -> None:
    response = await async_client.get(f"/post/{created_post["id"]}/comment")

    assert response.status_code == 200
    assert response.json() == [created_comment]


@pytest.mark.anyio
async def test_get_comments_on_post_empty(async_client: AsyncClient, created_post: dict) -> None:
    response = await async_client.get(f"/post/{created_post["id"]}/comment")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.anyio
async def test_get_post_with_comments(
    async_client: AsyncClient, created_post: dict, created_comment: dict
) -> None:
    response = await async_client.get(f"/post/{created_post["id"]}")

    assert response.status_code == 200
    assert response.json() == {
        "post": created_post,
        "comments": [created_comment],
    }


@pytest.mark.anyio
async def test_get_missing_post_with_comments(
    async_client: AsyncClient, created_post: dict, created_comment: dict
) -> None:
    response = await async_client.get("/post/2")

    assert response.status_code == 404
