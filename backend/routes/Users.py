import time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.db_depends import get_db
from backend.models import User
from backend.routes.auth.utils import get_current_user
from backend.schemas.users import UserWithPosts

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me", response_model=UserWithPosts)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    posts_out = []
    sorted_posts = sorted(current_user.posts, key=lambda post: post.created_at, reverse=True)

    for post in sorted_posts:
        liked = any(like.user_id == current_user.id for like in post.likes)

        posts_out.append({
            "id": post.id,
            "user_id": current_user.id,
            "nickname": current_user.nickname,
            "content": post.content,
            "created_at": post.created_at,
            "likes_count": len(post.likes),
            "comments_count": len(post.comments),
            "liked": liked,
        })

    time.sleep(1)
    return {
        "nickname": current_user.nickname,
        "posts": posts_out
    }


@router.get("/{user_id}", response_model=UserWithPosts)
def get_user_with_posts(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    posts_out = []
    sorted_posts = sorted(user.posts, key=lambda post: post.created_at, reverse=True)

    for post in sorted_posts:
        liked = any(like.user_id == current_user.id for like in post.likes)

        posts_out.append({
            "id": post.id,
            "user_id": user.id,
            "nickname": user.nickname,
            "content": post.content,
            "created_at": post.created_at,
            "likes_count": len(post.likes),
            "comments_count": len(post.comments),
            "liked": liked,
        })

    time.sleep(1)
    return {
        "nickname": user.nickname,
        "posts": posts_out
    }
