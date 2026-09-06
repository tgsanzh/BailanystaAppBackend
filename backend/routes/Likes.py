from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.db_depends import get_db
from backend.models import Post, Like, User, Notification
from backend.routes.auth.utils import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["Likes"]
)

@router.post("/{post_id}/like", status_code=201)
def like_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    existing_like = (
        db.query(Like)
        .filter(Like.post_id == post_id, Like.user_id == current_user.id)
        .first()
    )
    if existing_like:
        raise HTTPException(status_code=400, detail="You already liked this post")

    like = Like(user_id=current_user.id, post_id=post_id)
    db.add(like)
    db.commit()

    if current_user.id != post.user_id:
        owner = db.query(User).filter(User.id == post.user_id).first()
        if owner:
            notification_message = f"{current_user.nickname} поставил лайк вашему посту"
            notification = Notification(
                user_id=owner.id,
                post_id=post_id,
                message=notification_message,
                created_at=datetime.utcnow()
            )
            db.add(notification)
            db.commit()

    return {"message": "Post liked"}

@router.post("/{post_id}/unlike", status_code=200)
def unlike_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    like = (
        db.query(Like)
        .filter(Like.post_id == post_id, Like.user_id == current_user.id)
        .first()
    )
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")

    db.delete(like)
    db.commit()
    return {"message": "Post unliked"}
