from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app import models, schemas
from app.auth.auth_handler import (
    get_password_hash,
    verify_password,
    create_access_token
)
from sqlalchemy.future import select

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=schemas.User)
async def signup(user_data: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).where(models.User.username == user_data.username))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered.")

    hashed_password = await get_password_hash(user_data.password)
    new_user = models.User(username=user_data.username, hashed_password=hashed_password)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


@router.post("/login", response_model=schemas.Token)
async def login(user_data: schemas.UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).where(models.User.username == user_data.username))
    user = result.scalar_one_or_none()

    if not user or not await verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = await create_access_token({"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}
