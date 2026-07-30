from fastapi import FastAPI

from app.api import businesses
from app.api import auth
from app.api import dashboard
from app.api import services
from app.api import customers
from app.api import appointments

from app.database.database import engine
from app.database.database import Base

from app.models import user
from app.models import business
from app.models import service
from app.models import customer
from app.models import appointment


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="BeautyAI",
    description="AI-powered business assistant platform for small businesses"
)


# Business routes
app.include_router(
    businesses.router
)


# Authentication routes
app.include_router(
    auth.router
)


# Dashboard routes
app.include_router(
    dashboard.router
)


# Service routes
app.include_router(
    services.router
)


# Customer routes
app.include_router(
    customers.router
)


# Appointment routes
app.include_router(
    appointments.router
)


@app.get("/")
def home():
    return {
        "message": "BeautyAI API running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }