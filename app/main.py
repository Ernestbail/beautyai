from fastapi import FastAPI

app = FastAPI(
    title="BeautyAI",
    description="AI-powered business assistant for small businesses",
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
