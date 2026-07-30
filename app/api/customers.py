from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.customer import Customer
from app.models.business import Business
from app.models.user import User
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.auth.dependencies import get_current_user


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


# Get all customers belonging to the logged-in user's businesses
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
        .filter(Business.user_id == current_user.id)
        .all()
    )

    return customers


# Create a customer
@router.post(
    "/",
    response_model=CustomerResponse
)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
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


# Get one customer
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


# Update customer
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


# Delete customer
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
