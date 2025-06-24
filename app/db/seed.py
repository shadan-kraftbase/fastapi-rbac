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
            "role": Role.admin
        },
        {
            "email": "manager@example.com",
            "password": "manager123",
            "role": Role.manager
        },
        {
            "email": "user@example.com",
            "password": "user123",
            "role": Role.user
        },
    ]

    for user_data in users:
        user = User(
            email=user_data["email"],
            hashed_password=hash_password(user_data["password"]),
            role=user_data["role"],
            is_active=True
        )
        db.add(user)

    db.commit()
    db.close()
    print("Seed data inserted.")
