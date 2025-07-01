from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# 🔹 Category Schemas
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True


# 🔹 Supplier Schemas
class SupplierBase(BaseModel):
    name: str
    contact_info: Optional[str] = None
    address: Optional[str] = None

class SupplierCreate(SupplierBase):
    pass

class Supplier(SupplierBase):
    id: int

    class Config:
        from_attributes = True


# 🔹 Item Schemas
class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    quantity: int
    price: float
    category_id: int
    supplier_id: int

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# 🔹 StockTransaction Schemas
class StockTransactionBase(BaseModel):
    item_id: int
    change_type: str  # add / remove / adjust
    quantity: int
    user_id: int
    notes: Optional[str] = None

class StockTransactionCreate(StockTransactionBase):
    pass

class StockTransaction(StockTransactionBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True


# ------------------------------------------------------

# 🔹 User Schemas
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str  # plain password input

class User(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True

# -----------------------------------

# 🔐 JWT Auth Schemas
class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None