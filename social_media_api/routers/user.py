import logging

from fastapi import APIRouter, HTTPException, status

from social_media_api.database import database, user_table
from social_media_api.models.user import User, UserIn
from social_media_api.security import get_password_hash, get_user

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/register", response_model=User, status_code=201)
async def register(user: UserIn):
    if await get_user(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with that email already exists",
        )

    hashed_password = get_password_hash(user.password)
    query = user_table.insert().values(
        email=user.email,
        password=hashed_password,
    )

    user_id = await database.execute(query)

    return User(
        id=user_id,
        email=user.email
    )
