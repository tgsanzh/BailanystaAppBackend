import time
from turtle import delay
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import schemas

from backend import models
from backend.database.db_depends import get_db
from backend.models import Post
from backend.routes.auth.utils import get_current_user
from backend.schemas.posts import PostCreate, PostOut

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/")
def create_post(
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    post = models.Post(user_id=current_user.id, content=post_data.content)
    db.add(post)
    db.commit()
    db.refresh(post)
    return {
        "status_code": 200,
        "status": "success"
    }


@router.get("/", response_model=list[PostOut])
def get_all_posts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    posts = db.query(models.Post).join(models.User).order_by(models.Post.created_at.desc()).all()
    result = []

    for post in posts:
        liked = any(like.user_id == current_user.id for like in post.likes)

        result.append({
            "id": post.id,
            "user_id": post.author.id,
            "nickname": post.author.nickname,
            "content": post.content,
            "created_at": post.created_at,
            "likes_count": len(post.likes),
            "comments_count": len(post.comments),
            "liked": liked,
        })

    time.sleep(1)
    return result


@router.get("/search/{keyword}", response_model=list[PostOut])
def find_post(
    keyword: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    posts = (
        db.query(models.Post)
        .filter(models.Post.content.ilike(f"%{keyword}%"))
        .join(models.User)
        .order_by(models.Post.created_at.desc())
        .all()
    )

    result = []
    for post in posts:
        liked = any(like.user_id == current_user.id for like in post.likes)

        result.append({
            "id": post.id,
            "user_id": post.author.id,
            "nickname": post.author.nickname,
            "content": post.content,
            "created_at": post.created_at,
            "likes_count": len(post.likes),
            "comments_count": len(post.comments),
            "liked": liked,
        })

    time.sleep(1)
    return result