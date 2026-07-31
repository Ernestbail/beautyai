
from datetime import datetime, date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.models.business import Business
from app.models.customer import Customer
from app.models.service import Service
from app.models.appointment import Appointment
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentResponse
)
from app.auth.dependencies import get_current_user


router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)


# ============================================================
# GET ALL APPOINTMENTS
# Optional filters:
#   ?status=scheduled
#   ?status=confirmed
#   ?date=2026-08-15
# ============================================================

@router.get(
    "/",
    response_model=list[AppointmentResponse]
)
def get_appointments(
    status: str | None = Query(
        default=None,
        description="Filter by appointment status"
    ),
    appointment_date: date | None = Query(
        default=None,
        description="Filter by appointment date (YYYY-MM-DD)"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    query = (
        db.query(Appointment)
        .join(Business)
        .filter(
            Business.user_id == current_user.id
        )
    )

    # --------------------------------------------------------
    # Filter by status
    # Example:
    # /appointments/?status=scheduled
    # --------------------------------------------------------

    if status is not None:
        query = query.filter(
            Appointment.status == status
        )

    # --------------------------------------------------------
    # Filter by date
    # Example:
    # /appointments/?appointment_date=2026-08-15
    #
    # We use a date range so appointments on that day are
    # returned regardless of their time.
    # --------------------------------------------------------

    if appointment_date is not None:

        start_datetime = datetime.combine(
            appointment_date,
            datetime.min.time()
        )

        end_datetime = datetime.combine(
            appointment_date,
            datetime.max.time()
        )

        query = query.filter(
            Appointment.appointment_date >= start_datetime,
            Appointment.appointment_date <= end_datetime
        )

    # --------------------------------------------------------
    # Return newest appointment dates first
    # --------------------------------------------------------

    appointments = query.order_by(
        Appointment.appointment_date.asc()
    ).all()

    return appointments


# ============================================================
# CREATE APPOINTMENT
# ============================================================

@router.post(
    "/",
    response_model=AppointmentResponse
)
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # --------------------------------------------------------
    # Verify business belongs to logged-in user
    # --------------------------------------------------------

    business = db.query(Business).filter(
        Business.id == appointment.business_id,
        Business.user_id == current_user.id
    ).first()

    if business is None:
        raise HTTPException(
            status_code=404,
            detail="Business not found"
        )

    # --------------------------------------------------------
    # Verify customer belongs to same business
    # --------------------------------------------------------

    customer = db.query(Customer).filter(
        Customer.id == appointment.customer_id,
        Customer.business_id == appointment.business_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    # --------------------------------------------------------
    # Verify service belongs to same business
    # --------------------------------------------------------

    service = db.query(Service).filter(
        Service.id == appointment.service_id,
        Service.business_id == appointment.business_id
    ).first()

    if service is None:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    # --------------------------------------------------------
    # Create appointment
    # --------------------------------------------------------

    new_appointment = Appointment(
        business_id=appointment.business_id,
        customer_id=appointment.customer_id,
        service_id=appointment.service_id,
        appointment_date=appointment.appointment_date,
        status=appointment.status,
        notes=appointment.notes
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return new_appointment


# ============================================================
# GET ONE APPOINTMENT
# ============================================================

@router.get(
    "/{appointment_id}",
    response_model=AppointmentResponse
)
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    appointment = (
        db.query(Appointment)
        .join(Business)
        .filter(
            Appointment.id == appointment_id,
            Business.user_id == current_user.id
        )
        .first()
    )

    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    return appointment


# ============================================================
# UPDATE APPOINTMENT
# ============================================================

@router.put(
    "/{appointment_id}",
    response_model=AppointmentResponse
)
def update_appointment(
    appointment_id: int,
    appointment_data: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    appointment = (
        db.query(Appointment)
        .join(Business)
        .filter(
            Appointment.id == appointment_id,
            Business.user_id == current_user.id
        )
        .first()
    )

    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    # --------------------------------------------------------
    # Verify business belongs to logged-in user
    # --------------------------------------------------------

    business = db.query(Business).filter(
        Business.id == appointment_data.business_id,
        Business.user_id == current_user.id
    ).first()

    if business is None:
        raise HTTPException(
            status_code=404,
            detail="Business not found"
        )

    # --------------------------------------------------------
    # Verify customer belongs to selected business
    # --------------------------------------------------------

    customer = db.query(Customer).filter(
        Customer.id == appointment_data.customer_id,
        Customer.business_id == appointment_data.business_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    # --------------------------------------------------------
    # Verify service belongs to selected business
    # --------------------------------------------------------

    service = db.query(Service).filter(
        Service.id == appointment_data.service_id,
        Service.business_id == appointment_data.business_id
    ).first()

    if service is None:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    # --------------------------------------------------------
    # Update appointment
    # --------------------------------------------------------

    appointment.business_id = appointment_data.business_id
    appointment.customer_id = appointment_data.customer_id
    appointment.service_id = appointment_data.service_id
    appointment.appointment_date = appointment_data.appointment_date
    appointment.status = appointment_data.status
    appointment.notes = appointment_data.notes

    db.commit()
    db.refresh(appointment)

    return appointment


# ============================================================
# DELETE APPOINTMENT
# ============================================================

@router.delete(
    "/{appointment_id}"
)
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    appointment = (
        db.query(Appointment)
        .join(Business)
        .filter(
            Appointment.id == appointment_id,
            Business.user_id == current_user.id
        )
        .first()
    )

    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    db.delete(appointment)
    db.commit()

    return {
        "message": "Appointment deleted successfully"
    }