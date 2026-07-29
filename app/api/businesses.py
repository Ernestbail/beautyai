from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.business import Business
from app.models.user import User
from app.schemas.business import BusinessCreate, BusinessResponse
from app.auth.dependencies import get_current_user


router = APIRouter(
    prefix="/businesses",
    tags=["Businesses"]
)


# Get all businesses belonging to the logged-in user
@router.get(
    "/",
    response_model=list[BusinessResponse]
)
def get_businesses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    businesses = db.query(Business).filter(
        Business.user_id == current_user.id
    ).all()

    return businesses


# Get one specific business
@router.get(
    "/{business_id}",
    response_model=BusinessResponse
)
def get_business(
    business_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    business = db.query(Business).filter(
        Business.id == business_id,
        Business.user_id == current_user.id
    ).first()

    if business is None:
        raise HTTPException(
            status_code=404,
            detail="Business not found"
        )

    return business


# Create a new business
@router.post(
    "/",
    response_model=BusinessResponse
)
def create_business(
    business: BusinessCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_business = Business(
        name=business.name,
        owner=business.owner,
        email=business.email,
        website=business.website,
        booking_link=business.booking_link,
        hours=business.hours,
        policies=business.policies,
        user_id=current_user.id
    )

    db.add(new_business)
    db.commit()
    db.refresh(new_business)

    return new_business


# Update a business
@router.put(
    "/{business_id}",
    response_model=BusinessResponse
)
def update_business(
    business_id: int,
    business_data: BusinessCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    business = db.query(Business).filter(
        Business.id == business_id,
        Business.user_id == current_user.id
    ).first()

    if business is None:
        raise HTTPException(
            status_code=404,
            detail="Business not found"
        )

    business.name = business_data.name
    business.owner = business_data.owner
    business.email = business_data.email
    business.website = business_data.website
    business.booking_link = business_data.booking_link
    business.hours = business_data.hours
    business.policies = business_data.policies

    db.commit()
    db.refresh(business)

    return business
# Delete a business
@router.delete(
    "/{business_id}"
)
def delete_business(
    business_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    business = db.query(Business).filter(
        Business.id == business_id,
        Business.user_id == current_user.id
    ).first()

    if business is None:
        raise HTTPException(
            status_code=404,
            detail="Business not found"
        )

    db.delete(business)
    db.commit()

    return {
        "message": "Business deleted successfully"
    }