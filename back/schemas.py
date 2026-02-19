# backend/schemas.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# ------------------ User ------------------
class User(BaseModel):
    name: str
    email: EmailStr
    password: str

# ------------------ Item ------------------
class Item(BaseModel):
    item_name: str
    description: str
    date: str
    time: str
    location: str
    image_url: str
    contact_info: str
    type: str  # "lost" or "found"
    priority: Optional[bool] = False
    is_claimed: Optional[bool] = False
    wants_call: Optional[bool] = False  # Only relevant for lost items

# ------------------ Feedback ------------------
class Feedback(BaseModel):
    name: Optional[str] = "Anonymous"
    email: Optional[EmailStr] = None
    message: str
    date: Optional[str] = None  # Set automatically in backend
