# This file sets up the connection between our FastAPI app and PostgreSQL.
# Every other file that needs to talk to the database imports from here.

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environment variables from .env (like DATABASE_URL)
load_dotenv()

# Read the database connection string from .env
# Example: postgresql://postgres:postgres123@localhost:5432/nutrivision
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# The "engine" is what actually manages the connection to PostgreSQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal is a factory that creates new database sessions.
# A "session" is basically a temporary workspace to talk to the DB
# (query, insert, update, delete) — we open one per request.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the parent class that all our models (User, Meal, DetectedFood)
# will inherit from. SQLAlchemy uses this to know which Python classes
# should become database tables.
Base = declarative_base()


# This function gives a fresh DB session to each API request,
# and makes sure it's closed properly afterward — even if an error happens.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()