import pytest
from social_media_api import security


@pytest.mark.anyio
async def test_get_user(registered_user: dict):
    user = await security.get_user(registered_user["email"])

    assert user.email == registered_user["email"]


@pytest.mark.anyio
async def test_get_user_not_found():
    user = await security.get_user("user@not.found")

    assert user is None


@pytest.mark.anyio
def test_password_hashes():
    password = "password"
    assert security.verify_password(password, security.get_password_hash(password))
