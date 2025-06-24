from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import User, Role
from app.core.security import hash_password

def seed():
    db: Session = SessionLocal()

    # Check if any user exists
    if db.query(User).first():
        print("Seed data already exists.")
        db.close()
        return

    users = [
        {
            "email": "admin@example.com",
            "password": "admin123",
            "role": Role.ADMIN
        },
        {
            "email": "manager@example.com",
            "password": "manager123",
            "role": Role.MANAGER
        },
        {
            "email": "user@example.com",
            "password": "user123",
            "role": Role.USER
        },
    ]
