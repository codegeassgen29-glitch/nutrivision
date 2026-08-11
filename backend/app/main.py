# app/main.py
# ---------------------------------------------------------
# This file is the ENTRYPOINT of our backend server.
# When we run `uvicorn app.main:app`, Python loads this file
# and starts serving whatever is inside the `app` variable.
#
# Think of this file as the "front door" of the kitchen (backend).
# It doesn't cook anything itself - it just sets up the kitchen
# and tells each station (route file) where to stand.
# ---------------------------------------------------------
# NOTE: Ensure FastAPI is installed via: pip install fastapi uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# We create the main FastAPI application object.
# `title` and `description` show up automatically in the
# interactive docs FastAPI generates for us at /docs
app = FastAPI(
    title="NutriVision AI",
    description="AI-powered food recognition and nutrition analysis platform",
    version="0.1.0",
)

# ---------------------------------------------------------
# CORS (Cross-Origin Resource Sharing)
# ---------------------------------------------------------
# By default, browsers BLOCK a webpage running on one address
# (e.g. http://localhost:5173, our React app) from making
# requests to a server running on a different address
# (e.g. http://localhost:8000, our FastAPI backend).
#
# This is a browser security feature. Since our frontend and
# backend genuinely ARE different addresses during development,
# we must explicitly tell the backend "it's okay, trust requests
# coming from this frontend address."
#
# In production we will restrict this to our real domain name
# instead of allowing everything.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # our Vite dev server address
    allow_credentials=True,
    allow_methods=["*"],  # allow GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],
)


# ---------------------------------------------------------
# A basic route to prove the server is alive.
# ---------------------------------------------------------
# `@app.get("/")` means: "when someone visits the root URL
# with a GET request, run the function right below this line."
@app.get("/")
def read_root():
    # FastAPI automatically converts this Python dictionary
    # into a JSON response for us - no manual conversion needed.
    return {"message": "Welcome to NutriVision AI API"}


# ---------------------------------------------------------
# A health check route.
# ---------------------------------------------------------
# This is a common pattern in real production systems.
# Deployment tools (Docker, Render, load balancers) periodically
# call /health to check "is this server still alive and responding?"
# If it stops responding, the platform can automatically restart it.
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/version")
def get_version():
    return {"version": "0.1.0"}
