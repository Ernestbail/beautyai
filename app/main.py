from fastapi import FastAPI

from app.api import businesses
from app.api import auth
from app.api import dashboard
from app.api import services
from app.api import customers

from app.database.database import engine
from app.database.database import Base

from app.models import user
from app.models import business
from app.models import service
from app.models import customer


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="BeautyAI",
    description="AI-powered business assistant platform for small businesses"
)


app.include_router(
    businesses.router
)


app.include_router(
    auth.router
)


app.include_router(
    dashboard.router
)


app.include_router(
    services.router
)


app.include_router(
    customers.router
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