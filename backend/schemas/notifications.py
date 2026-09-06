from pydantic import BaseModel
from datetime import datetime

class NotificationOut(BaseModel):
    id: int
    message: str
    post_id: int
    created_at: datetime

    class Config:
        orm_mode = True