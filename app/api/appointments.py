from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
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


# Get all appointments belonging to the logged-in user's businesses
@router.get(
    "/",
    response_model=list[AppointmentResponse]
)
def get_appointments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    appointments = (
        db.query(Appointment)
        .join(Business)
        .filter(
            Business.user_id == current_user.id
        )
        .all()
    )

    return appointments


# Create an appointment
@router.post(
    "/",
    response_model=AppointmentResponse
)
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Verify business belongs to logged-in user
    business = db.query(Business).filter(
        Business.id == appointment.business_id,
        Business.user_id == current_user.id
    ).first()

    if business is None:
        raise HTTPException(
            status_code=404,
            detail="Business not found"
        )

    # Verify customer belongs to the same business
    customer = db.query(Customer).filter(
        Customer.id == appointment.customer_id,
        Customer.business_id == appointment.business_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    # Verify service belongs to the same business
    service = db.query(Service).filter(
        Service.id == appointment.service_id,
        Service.business_id == appointment.business_id
    ).first()

    if service is None:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

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


# Get one appointment
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


# Update appointment
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

    # Verify the new business belongs to the logged-in user
    business = db.query(Business).filter(
        Business.id == appointment_data.business_id,
        Business.user_id == current_user.id
    ).first()

    if business is None:
        raise HTTPException(
            status_code=404,
            detail="Business not found"
        )

    # Verify customer belongs to the selected business
    customer = db.query(Customer).filter(
        Customer.id == appointment_data.customer_id,
        Customer.business_id == appointment_data.business_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    # Verify service belongs to the selected business
    service = db.query(Service).filter(
        Service.id == appointment_data.service_id,
        Service.business_id == appointment_data.business_id
    ).first()

    if service is None:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    appointment.business_id = appointment_data.business_id
    appointment.customer_id = appointment_data.customer_id
    appointment.service_id = appointment_data.service_id
    appointment.appointment_date = appointment_data.appointment_date
    appointment.status = appointment_data.status
    appointment.notes = appointment_data.notes

    db.commit()
    db.refresh(appointment)

    return appointment


# Delete appointment
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

