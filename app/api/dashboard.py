from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.models.business import Business
from app.auth.dependencies import get_current_user


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    businesses = db.query(Business).filter(
        Business.user_id == current_user.id
    ).all()

    return {
        "user": {
            "id": current_user.id,
            "full_name": current_user.full_name,
            "email": current_user.email
        },
        "businesses": [
            {
                "id": business.id,
                "name": business.name,
                "owner": business.owner,
                "email": business.email,
                "website": business.website,
                "booking_link": business.booking_link,
                "hours": business.hours,
                "policies": business.policies
            }
            for business in businesses
        ]
    }
