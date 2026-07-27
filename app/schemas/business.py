from pydantic import BaseModel


class BusinessCreate(BaseModel):
    name: str
    owner: str
    email: str
    website: str
    booking_link: str
    hours: str
    policies: str


class BusinessResponse(BusinessCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True