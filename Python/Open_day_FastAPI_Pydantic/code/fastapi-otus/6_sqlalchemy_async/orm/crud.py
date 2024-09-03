from hashlib import sha512

from sqlalchemy.ext.asyncio import AsyncSession
from . import models
from sqlalchemy import select


class Users:
    @staticmethod
    async def get(db: AsyncSession, user_id: int):
        return (await db.execute(select(models.User).filter(models.User.id == user_id))).scalars().first()

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str):
        return (await db.execute(select(models.User).filter(models.User.email == email))).scalars().first()

    @staticmethod
    async def all(db: AsyncSession, skip: int = 0, limit: int = 100):
        return (await db.execute(select(models.User).offset(skip).limit(limit))).scalars().all()

    @staticmethod
    async def create(db: AsyncSession, email: str, password: str):
        db_user = models.User(email=email, hashed_password=sha512(password.encode('utf-8')).hexdigest())
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    class Items:
        @staticmethod
        async def all(db: AsyncSession, skip: int = 0, limit: int = 100):
            return (await db.execute(select(models.Item).offset(skip).limit(limit))).scalars().first()

        @staticmethod
        async def create(db: AsyncSession, item_title: str, item_description: str, user_id: int):
            db_item = models.Item(**{'title': item_title, 'description': item_description}, owner_id=user_id)
            db.add(db_item)
            await db.commit()
            await db.refresh(db_item)
            return db_item