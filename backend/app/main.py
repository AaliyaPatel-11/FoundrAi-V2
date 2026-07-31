from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import FRONTEND_ORIGIN
from app.api.chat import router as chat_router

app = FastAPI(
    title="FondrAI API",
    description="Backend API for FondrAI - AI Startup Co-founder",
    version="1.0.0"
)

# CORS configuration
# Allows specified origin or defaults to local Vite app during dev
origins = []
if FRONTEND_ORIGIN:
    # Allow comma-separated multiple origins if configured
    origins = [origin.strip() for origin in FRONTEND_ORIGIN.split(",") if origin.strip()]

# Always allow standard Vite dev server origin for ease of development
if "http://localhost:5173" not in origins:
    origins.append("http://localhost:5173")
if "http://127.0.0.1:5173" not in origins:
    origins.append("http://127.0.0.1:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Chat router
app.include_router(chat_router)

@app.get("/")
def read_root():
    return {
        "name": "FondrAI",
        "status": "online"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
