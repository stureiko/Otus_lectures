from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://otus:otus@localhost/ormasync"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
)
SessionLocal = async_sessionmaker(engine, autoflush=True, expire_on_commit=False)

Base = declarative_base()