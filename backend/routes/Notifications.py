from fastapi import APIRouter, Depends
from requests import Session

from backend.database.db_depends import get_db
from backend.models import User, Notification
from backend.routes.auth.utils import get_current_user
from backend.schemas.notifications import NotificationOut

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)

@router.get("/", response_model=list[NotificationOut])
def get_user_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notifications = (
        db.query(Notification)
        .filter(Notification.user_id == current_user.id)
        .order_by(Notification.created_at.desc())
        .all()
    )
    return notifications