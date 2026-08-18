# This file handles user profile and account settings.
# All routes here require the user to be logged in.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user, hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserOut, UserUpdate, PasswordUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserOut)
def get_my_profile(current_user: User = Depends(get_current_user)):
    """
    Returns the logged-in user's profile info.
    (This duplicates /auth/me from earlier - having it under /users
    is more conventional REST-wise, but both can coexist.)
    """
    return current_user


@router.put("/me", response_model=UserOut)
def update_my_profile(
    update_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Updates the logged-in user's editable profile fields.
    Currently just full_name - can expand later (bio, avatar, etc.)
    """
    if update_data.full_name is not None:
        current_user.full_name = update_data.full_name

    db.commit()
    db.refresh(current_user)

    return current_user


@router.put("/me/password", status_code=status.HTTP_200_OK)
def change_password(
    password_data: PasswordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Changes the logged-in user's password.
    Requires the current password to be correct, as a safety check
    (prevents someone with a stolen/leaked token from silently
    locking the real owner out).
    """
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )

    current_user.hashed_password = hash_password(password_data.new_password)
    db.commit()

    return {"message": "Password updated successfully"}