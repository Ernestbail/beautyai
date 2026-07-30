from pydantic import BaseModel
from typing import Optional


class ServiceBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    duration: int


class ServiceCreate(ServiceBase):
    business_id: int


class ServiceResponse(ServiceBase):
    id: int
    business_id: int

    class Config:
        from_attributes = True
