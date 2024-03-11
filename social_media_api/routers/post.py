from fastapi import APIRouter, HTTPException
from social_media_api.models.post import (
    Comment,
    CommentIn,
    UserPost,
    UserPostIn,
    UserPostWithComments,
)


router = APIRouter()

# Local storage, database to be implemented in the future
post_table = {}
comment_table = {}


def find_post(post_id: int):
    return post_table.get(post_id)


def get_last_id(table):
    return len(table)


@router.post("/post", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn):
    data = post.model_dump()  # Using model_dump because dict is deprecated
    last_record_id = get_last_id(post_table)
    new_post = {**data, "id": last_record_id}

    post_table[last_record_id] = new_post

    return new_post


@router.get("/post", response_model=list[UserPost])
async def get_all_posts():
    return list(post_table.values())


@router.post("/comment", response_model=Comment, status_code=201)
async def create_comment(comment: CommentIn):
    post = find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    data = comment.model_dump()
    last_record_id = get_last_id(comment_table)
    comment_post = {**data, "id": last_record_id, "post_id": comment.post_id}

    comment_table[last_record_id] = comment_post

    return comment_post


@router.get("/post/{post_id}/comment", response_model=list[Comment])
async def get_comments_on_post(post_id: int):
    post = find_post(post_id)
    if not post:
        return HTTPException(status_code=404, detail="Post not found")

    return [comment for comment in comment_table.values() if comment["post_id"] == post_id]


@router.get("/post/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {
        "post": post,
        "comments": await get_comments_on_post(post_id),
    }
