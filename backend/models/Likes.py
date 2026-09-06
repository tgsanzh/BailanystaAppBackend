from datetime import datetime

from sqlalchemy import UniqueConstraint, DateTime, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from backend.database.db import Base


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")

    __table_args__ = (
        UniqueConstraint('user_id', 'post_id', name='uix_user_post_like'),
    )