# This file handles two core security jobs:
# 1. Hashing and verifying passwords (so we never store plain text passwords)
# 2. Creating and verifying JWT tokens (so users stay "logged in" securely)
# 3. Providing a reusable dependency (get_current_user) to protect routes

import os
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError
from dotenv import load_dotenv

from app.core.database import get_db
from app.models.user import User

load_dotenv()

# Read JWT settings from .env
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# This sets up bcrypt as our password hashing algorithm.
# bcrypt automatically adds "salt" (random data) so identical
# passwords never produce the same hash.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# This tells FastAPI: "tokens are obtained via /auth/login, and
# expected as 'Authorization: Bearer <token>' on protected routes."
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def hash_password(password: str) -> str:
    """Takes a plain text password and returns a secure hash to store in the DB."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Checks if a plain text password matches the stored hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """
    Creates a JWT token containing the given data (usually the user's ID).
    The token is signed with SECRET_KEY, so we can trust it wasn't tampered with.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict | None:
    """
    Verifies a JWT token and returns its data if valid.
    Returns None if the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    This is a FastAPI dependency. Any route that adds
    `current_user: User = Depends(get_current_user)`
    will automatically:
    1. Extract the token from the Authorization header
    2. Decode and verify it
    3. Look up the matching user in the database
    4. Return that User object (or raise 401 if anything fails)
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    return user