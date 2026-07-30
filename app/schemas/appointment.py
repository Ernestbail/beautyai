from datetime import datetime

from pydantic import BaseModel


class AppointmentCreate(BaseModel):
    business_id: int
    customer_id: int
    service_id: int
    appointment_date: datetime
    status: str = "scheduled"
    notes: str | None = None


class AppointmentResponse(BaseModel):
    id: int
    business_id: int
    customer_id: int
    service_id: int
    appointment_date: datetime
    status: str
    notes: str | None = None

    class Config:
        from_attributes = True
