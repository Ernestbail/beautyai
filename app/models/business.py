from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Business(Base):
    __tablename__ = "businesses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        index=True
    )

    owner = Column(
        String
    )

    email = Column(
        String
    )

    website = Column(
        String
    )

    booking_link = Column(
        String
    )

    hours = Column(
        String
    )

    policies = Column(
        String
    )

    # Connect business to user
    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    user = relationship(
        "User",
        back_populates="businesses"
    )