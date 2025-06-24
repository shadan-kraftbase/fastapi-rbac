from sqlalchemy.orm import Session
from app.db.models import User, Role as DBRole
from app.core.security import hash_password, verify_password
from app.schemas.user import UserCreate
from uuid import UUID
from sqlalchemy.orm import Session
from app.db.models import User
from app.schemas.user import UserCreate


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_in: UserCreate):
    hashed = hash_password(user_in.password)
    db_role = DBRole(user_in.role.value)
    user = User(email=user_in.email, hashed_password=hashed, role=db_role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_id(db: Session, user_id: UUID) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def get_all_users(db: Session):
    return db.query(User).all()

def update_user(db: Session, db_user: User, update_data: dict) -> User:
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, db_user: User):
    db.delete(db_user)
    db.commit()
