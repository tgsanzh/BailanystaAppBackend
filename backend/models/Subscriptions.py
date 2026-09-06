from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship

from backend.database.db import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    subscriber_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subscribed_to_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    subscriber = relationship("User", foreign_keys=[subscriber_id], back_populates="subscriptions")
    subscribed_to = relationship("User", foreign_keys=[subscribed_to_id], back_populates="subscribers")

    __table_args__ = (
        UniqueConstraint('subscriber_id', 'subscribed_to_id', name='uix_subscriber_subscribed_to'),
    )