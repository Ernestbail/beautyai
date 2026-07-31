
from datetime import datetime

from pydantic import BaseModel


class CustomerCreate(BaseModel):
    name: str
    email: str | None = None
    phone: str | None = None
    notes: str | None = None
    business_id: int


class CustomerResponse(BaseModel):
    id: int
    business_id: int
    name: str
    email: str | None = None
    phone: str | None = None
    notes: str | None = None

    class Config:
        from_attributes = True


# ============================================================
# CUSTOMER APPOINTMENT HISTORY
# ============================================================

class CustomerAppointmentHistory(BaseModel):
    id: int
    service_id: int
    service_name: str | None = None
    price: float
    duration: int | None = None
    appointment_date: datetime
    status: str
    notes: str | None = None


# ============================================================
# CUSTOMER STATISTICS
# ============================================================

class CustomerStatistics(BaseModel):
    total_appointments: int
    scheduled_appointments: int
    confirmed_appointments: int
    completed_appointments: int
    cancelled_appointments: int
    upcoming_appointments: int
    estimated_customer_value: float


# ============================================================
# CUSTOMER CRM DETAILS
# ============================================================

class CustomerDetailsResponse(BaseModel):
    id: int
    business_id: int
    name: str
    email: str | None = None
    phone: str | None = None
    notes: str | None = None

    statistics: CustomerStatistics

    appointments: list[CustomerAppointmentHistory]

    class Config:
        from_attributes = True