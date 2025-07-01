# app/routers/inventory.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import crud, schemas, database

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)

get_db = database.get_db

# --------------------------
# CATEGORY ROUTES
# --------------------------
@router.post("/categories/", response_model=schemas.Category)
async def create_category(category: schemas.CategoryCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_category(db=db, category=category)

@router.get("/categories/", response_model=List[schemas.Category])
async def get_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_categories(db=db, skip=skip, limit=limit)

@router.get("/categories/{category_id}", response_model=schemas.Category)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    db_category = await crud.get_category(db, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

# --------------------------
# SUPPLIER ROUTES
# --------------------------
@router.post("/suppliers/", response_model=schemas.Supplier)
async def create_supplier(supplier: schemas.SupplierCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_supplier(db=db, supplier=supplier)

@router.get("/suppliers/", response_model=List[schemas.Supplier])
async def get_suppliers(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_suppliers(db=db, skip=skip, limit=limit)

@router.get("/suppliers/{supplier_id}", response_model=schemas.Supplier)
async def get_supplier(supplier_id: int, db: AsyncSession = Depends(get_db)):
    db_supplier = await crud.get_supplier(db, supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier

# --------------------------
# ITEM ROUTES
# --------------------------
@router.post("/items/", response_model=schemas.Item)
async def create_item(item: schemas.ItemCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_item(db=db, item=item)

@router.get("/items/", response_model=List[schemas.Item])
async def get_items(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await crud.get_items(db=db, skip=skip, limit=limit)

@router.get("/items/{item_id}", response_model=schemas.Item)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    db_item = await crud.get_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.put("/items/{item_id}", response_model=schemas.Item)
async def update_item(item_id: int, item: schemas.ItemCreate, db: AsyncSession = Depends(get_db)):
    updated_item = await crud.update_item(db=db, item_id=item_id, item_update=item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@router.delete("/items/{item_id}", response_model=schemas.Item)
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    deleted_item = await crud.delete_item(db=db, item_id=item_id)
    if deleted_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return deleted_item
