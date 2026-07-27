from fastapi import FastAPI

from app.database.database import engine, Base

# Import models so tables are created
from app.models.business import Business
from app.models.user import User

# Import API routers
from app.api.businesses import router as business_router
from app.api.auth import router as auth_router


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="BeautyAI",
    description="AI-powered business assistant platform for small businesses",
    version="1.0.0"
)


# Register API routes
app.include_router(business_router)
app.include_router(auth_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to BeautyAI"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }