# app/database.py

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from app.settings import settings

# 🌱 Load environment variables
load_dotenv()

#  Async DB URL from .env
#  Use async URL!
# For SQLite:     sqlite+aiosqlite:///./inventory.db
# For PostgreSQL: postgresql+asyncpg://postgres:1234@localhost/inventory_db
# ✅ Construct the async PostgreSQL URL using settings
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@localhost:5432/inventory_db"


# 🚀 Create async engine
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,  # Optional: logs SQL queries
)

# 🔁 Async Session maker
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# 📦 Base class for ORM models
Base = declarative_base()

# 📤 Async Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
