import pydantic
from pydantic import BaseModel

from backend.schemas.posts import PostOut


class UserWithPosts(BaseModel):
    nickname: str
    posts: list[PostOut]

    class Config:
        orm_mode = True