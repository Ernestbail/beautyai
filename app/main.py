from fastapi import FastAPI

from app.api import businesses
from app.api import auth

from app.database.database import engine
from app.database.database import Base

from app.models import user
from app.models import business


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
