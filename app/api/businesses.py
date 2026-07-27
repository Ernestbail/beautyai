from app.auth.security import get_current_user
from app.models.user import User
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.business import Business
from app.schemas.business import BusinessCreate, BusinessResponse


router = APIRouter(
    prefix="/businesses",
    tags=["Businesses"]
)


@router.post("/", response_model=BusinessResponse)
def create_business(
    business: BusinessCreate,
    db: Session = Depends(get_db)
):

    new_business = Business(
        name=business.name,
        owner=business.owner,
        email=business.email,
        website=business.website,
        booking_link=business.booking_link,
        hours=business.hours,
        policies=business.policies,
        user_id=business.user_id
    )

    db.add(new_business)
    db.commit()
    db.refresh(new_business)

    return new_business

@router.get("/", response_model=list[BusinessResponse])
def get_businesses(
    db: Session = Depends(get_db)
):

    businesses = db.query(Business).all()

    return businesses
