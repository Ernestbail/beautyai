
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.customer import Customer
from app.models.business import Business
from app.models.user import User
from app.models.appointment import Appointment
from app.models.service import Service
from app.schemas.customer import (
    CustomerCreate,
    CustomerResponse,
    CustomerDetailsResponse
)
from app.auth.dependencies import get_current_user


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


# ============================================================
# GET ALL CUSTOMERS
# ============================================================

@router.get(
    "/",
    response_model=list[CustomerResponse]
)
def get_customers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    customers = (
        db.query(Customer)
        .join(Business)
        .filter(
            Business.user_id == current_user.id
        )
        .all()
    )

    return customers


# ============================================================
# CREATE CUSTOMER
# ============================================================

@router.post(
    "/",
    response_model=CustomerResponse
)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Verify business belongs to logged-in user
    business = db.query(Business).filter(
        Business.id == customer.business_id,
        Business.user_id == current_user.id
    ).first()

    if business is None:
        raise HTTPException(
            status_code=404,
            detail="Business not found"
        )

    new_customer = Customer(
        name=customer.name,
        email=customer.email,
        phone=customer.phone,
        notes=customer.notes,
        business_id=customer.business_id
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


# ============================================================
# GET ONE CUSTOMER
# ============================================================

@router.get(
    "/{customer_id}",
    response_model=CustomerResponse
)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    customer = (
        db.query(Customer)
        .join(Business)
        .filter(
            Customer.id == customer_id,
            Business.user_id == current_user.id
        )
        .first()
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer


# ============================================================
# CUSTOMER CRM DETAILS
# ============================================================

@router.get(
    "/{customer_id}/details",
    response_model=CustomerDetailsResponse
)
def get_customer_details(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # --------------------------------------------------------
    # Find customer and make sure they belong to this user's
    # business.
    # --------------------------------------------------------

    customer = (
        db.query(Customer)
        .join(Business)
        .filter(
            Customer.id == customer_id,
            Business.user_id == current_user.id
        )
        .first()
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    # --------------------------------------------------------
    # Get all appointments for this customer.
    # --------------------------------------------------------

    appointments = (
        db.query(Appointment)
        .filter(
            Appointment.customer_id == customer.id,
            Appointment.business_id == customer.business_id
        )
        .order_by(
            Appointment.appointment_date.desc()
        )
        .all()
    )

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    total_appointments = len(appointments)

    scheduled_appointments = sum(
        1
        for appointment in appointments
        if appointment.status == "scheduled"
    )

    confirmed_appointments = sum(
        1
        for appointment in appointments
        if appointment.status == "confirmed"
    )

    completed_appointments = sum(
        1
        for appointment in appointments
        if appointment.status == "completed"
    )

    cancelled_appointments = sum(
        1
        for appointment in appointments
        if appointment.status == "cancelled"
    )

    # --------------------------------------------------------
    # Upcoming appointments
    # --------------------------------------------------------

    now = datetime.now()

    upcoming_appointments = [
        appointment
        for appointment in appointments
        if appointment.appointment_date >= now
        and appointment.status not in ["cancelled", "completed"]
    ]

    # --------------------------------------------------------
    # Calculate estimated customer value.
    #
    # We get the price from the related service.
    # --------------------------------------------------------

    total_value = 0.0

    appointment_history = []

    for appointment in appointments:

        service = (
            db.query(Service)
            .filter(
                Service.id == appointment.service_id,
                Service.business_id == customer.business_id
            )
            .first()
        )

        service_name = None
        service_price = 0.0
        service_duration = None

        if service is not None:
            service_name = service.name
            service_price = service.price
            service_duration = service.duration

            # Do not count cancelled appointments toward
            # estimated customer value.
            if appointment.status != "cancelled":
                total_value += service.price

        appointment_history.append(
            {
                "id": appointment.id,
                "service_id": appointment.service_id,
                "service_name": service_name,
                "price": service_price,
                "duration": service_duration,
                "appointment_date": appointment.appointment_date,
                "status": appointment.status,
                "notes": appointment.notes
            }
        )

    # --------------------------------------------------------
    # Return complete CRM profile
    # --------------------------------------------------------

    return {
        "id": customer.id,
        "business_id": customer.business_id,
        "name": customer.name,
        "email": customer.email,
        "phone": customer.phone,
        "notes": customer.notes,

        "statistics": {
            "total_appointments": total_appointments,
            "scheduled_appointments": scheduled_appointments,
            "confirmed_appointments": confirmed_appointments,
            "completed_appointments": completed_appointments,
            "cancelled_appointments": cancelled_appointments,
            "upcoming_appointments": len(upcoming_appointments),
            "estimated_customer_value": total_value
        },

        "appointments": appointment_history
    }


# ============================================================
# UPDATE CUSTOMER
# ============================================================

@router.put(
    "/{customer_id}",
    response_model=CustomerResponse
)
def update_customer(
    customer_id: int,
    customer_data: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    customer = (
        db.query(Customer)
        .join(Business)
        .filter(
            Customer.id == customer_id,
            Business.user_id == current_user.id
        )
        .first()
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    # Verify new business belongs to logged-in user
    business = db.query(Business).filter(
        Business.id == customer_data.business_id,
        Business.user_id == current_user.id
    ).first()

    if business is None:
        raise HTTPException(
            status_code=404,
            detail="Business not found"
        )

    customer.name = customer_data.name
    customer.email = customer_data.email
    customer.phone = customer_data.phone
    customer.notes = customer_data.notes
    customer.business_id = customer_data.business_id

    db.commit()
    db.refresh(customer)

    return customer


# ============================================================
# DELETE CUSTOMER
# ============================================================

@router.delete(
    "/{customer_id}"
)
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    customer = (
        db.query(Customer)
        .join(Business)
        .filter(
            Customer.id == customer_id,
            Business.user_id == current_user.id
        )
        .first()
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    db.delete(customer)
    db.commit()

    return {
        "message": "Customer deleted successfully"
    }