from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

from backend.database.db_depends import get_db
from backend.models import Post, Comment, User, Notification
from backend.routes.auth.utils import get_current_user
from backend.schemas.comments import CommentOut, CommentCreate

router = APIRouter(
    prefix="/posts",
    tags=["Comments"]
)

@router.get("/{post_id}/comments", response_model=list[CommentOut])
def get_comments_by_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    comments = (
        db.query(Comment)
        .filter(Comment.post_id == post_id)
        .join(User)
        .order_by(desc(Comment.created_at))
        .all()
    )

    result = []
    for comment in comments:
        result.append({
            "id": comment.id,
            "user_id": comment.user_id,
            "nickname": comment.user.nickname,
            "content": comment.content,
            "created_at": comment.created_at
        })

    return result

@router.post("/{post_id}/comments", status_code=201)
def create_comment(
    post_id: int,
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    comment = Comment(
        content=comment_data.content,
        post_id=post_id,
        user_id=current_user.id,
        created_at=datetime.utcnow()
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

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

    return {
        "id": comment.id,
        "nickname": current_user.nickname,
        "content": comment.content,
        "created_at": comment.created_at
    }