from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.models.Users import User
from backend.routes.auth.utils import verify_password, create_access_token, hash_password
from backend.schemas.auth import UserCreate, UserLogin, Token
from datetime import timedelta

from backend.database.db_depends import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.nickname == user_data.nickname).first()
    if user:
        raise HTTPException(status_code=400, detail="Nickname already registered")

    new_user = User(
        nickname=user_data.nickname,
        password=hash_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(data={"sub": str(new_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.nickname == user_data.nickname).first()
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect phone number or password")

    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=timedelta(minutes=600))
    return {"access_token": access_token, "token_type": "bearer"}
