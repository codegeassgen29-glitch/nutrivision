# This file defines the authentication endpoints:
# - /auth/signup -> creates a new user
# - /auth/login  -> verifies credentials and returns a JWT token

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.core.security import hash_password, verify_password, create_access_token

# APIRouter lets us group related routes together and plug them
# into the main FastAPI app later (in main.py) with a prefix like "/auth"
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Creates a new user account.
    - Receives email, password, full_name (validated by UserCreate schema)
    - Hashes the password before storing it
    - Returns the created user (without the password, via UserOut schema)
    """

    # Hash the plain password the user sent us
    hashed_pw = hash_password(user_data.password)

    # Build a new User model instance (this is NOT saved to DB yet)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_pw,
        full_name=user_data.full_name,
    )

    db.add(new_user)  # stage the insert
    try:
        db.commit()  # actually save to the database
    except IntegrityError:
        # This happens if the email already exists (unique constraint)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    db.refresh(new_user)  # reload new_user with DB-generated fields (id, created_at)
    return new_user


@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    """
    Verifies email + password, and if correct, returns a JWT access token.
    """

    # Look up the user by email
    user = db.query(User).filter(User.email == email).first()

    # If no user found, OR password doesn't match -> reject
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    # Create a JWT token containing the user's ID (as "sub" = subject)
    access_token = create_access_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}