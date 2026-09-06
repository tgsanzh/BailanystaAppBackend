from datetime import datetime

from pydantic import BaseModel


class CommentOut(BaseModel):
    id: int
    nickname: str
    user_id: int
    content: str
    created_at: datetime

    class Config:
        orm_mode = True

class CommentCreate(BaseModel):
    content: str