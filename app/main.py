from fastapi import FastAPI
from app.database.database import engine, Base
from app.models.business import Business

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BeautyAI",
    description="AI-powered business assistant platform for small businesses",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to BeautyAI 🚀"
    }


@app.get("/health")
def health_check():
    return {
        "status": "BeautyAI is running"
    }