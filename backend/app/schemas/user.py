from pydantic import BaseModel, EmailStr
from datetime import datetime

# This is what a client sends us when signing up
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None

# This is what we send back to the client (never includes password)
class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None
    created_at: datetime

    class Config:
        from_attributes = True  # lets Pydantic read directly from SQLAlchemy objects