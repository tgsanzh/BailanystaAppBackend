from pydantic import BaseModel

class UserCreate(BaseModel):
    nickname: str
    password: str

class UserLogin(BaseModel):
    nickname: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
