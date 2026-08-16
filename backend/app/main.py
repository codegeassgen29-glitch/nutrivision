from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import meal
from app.api import auth

app = FastAPI(
    title="NutriVision AI",
    description="AI-powered food recognition and nutrition analysis platform",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(meal.router)

# ---------------------------------------------------------
# Register route modules
# ---------------------------------------------------------

@app.get("/")
def read_root():
    return {"message": "Welcome to NutriVision AI API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/version")
def get_version():
    return {"version": "0.1.0"}