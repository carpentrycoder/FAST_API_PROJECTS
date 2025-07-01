from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import EmailStr, Field as PydField

# 🔹 Shared Base class (used for both Create and DB models)
class UserBase(SQLModel):
    name: str = PydField(min_length=2, max_length=50)
    email: EmailStr  # validates email format
    age: int = PydField(ge=10, le=100)  # age 10–100

# 🔹 DB model for SQLite (adds ID + makes table=True)
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

# 🔹 Input model for POST requests (no id)
class UserCreate(UserBase):
    pass
