from hashlib import sha512

from sqlalchemy.orm import Session

from . import models


class Users:
    @staticmethod
    def get(db: Session, user_id: int):
        return db.query(models.User).filter(models.User.id == user_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(models.User).filter(models.User.email == email).first()

    @staticmethod
    def all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.User).offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, email: str, password: str):
        db_user = models.User(email=email, hashed_password=sha512(password.encode('utf-8')).hexdigest())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    class Items:
        @staticmethod
        def all(db: Session, skip: int = 0, limit: int = 100):
            return db.query(models.Item).offset(skip).limit(limit).all()

        @staticmethod
        def create(db: Session, item_title: str, item_description: str, user_id: int):
            db_item = models.Item(**{'title': item_title, 'description': item_description}, owner_id=user_id)
            db.add(db_item)
            db.commit()
            db.refresh(db_item)
            return db_item