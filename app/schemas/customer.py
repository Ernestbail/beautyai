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
