from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship

from backend.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")

    subscriptions = relationship(
        "Subscription",
        foreign_keys="[Subscription.subscriber_id]",
        back_populates="subscriber",
        cascade="all, delete-orphan"
    )
    subscribers = relationship(
        "Subscription",
        foreign_keys="[Subscription.subscribed_to_id]",
        back_populates="subscribed_to",
        cascade="all, delete-orphan"
    )

