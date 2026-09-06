from datetime import datetime

from pydantic import BaseModel


class PostCreate(BaseModel):
    content: str

class PostOut(BaseModel):
    id: int
    user_id: int
    nickname: str
    content: str
    created_at: datetime
    likes_count: int
    comments_count: int
    liked: bool

    class Config:
        orm_mode = True
