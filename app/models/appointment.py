from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    business_id = Column(
        Integer,
        ForeignKey("businesses.id"),
        nullable=False
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False
    )

    service_id = Column(
        Integer,
        ForeignKey("services.id"),
        nullable=False
    )

    appointment_date = Column(
        DateTime,
        nullable=False
    )

    status = Column(
        String,
        nullable=False,
        default="scheduled"
    )

    notes = Column(
        String,
        nullable=True
    )

    # Connect appointment to business
    business = relationship(
        "Business",
        back_populates="appointments"
    )

    # Connect appointment to customer
    customer = relationship(
        "Customer",
        back_populates="appointments"
    )

    # Connect appointment to service
    service = relationship(
        "Service",
        back_populates="appointments"
    )