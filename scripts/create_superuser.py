import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import engine
from app.models.user import User
from app.core.security import get_password_hashed
def create_superuser():
    print("--- Create Admin Superuser ---")
    name = input("Enter admin name: ")
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")

    with Session(engine) as db:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            print(f"User with email {email} already exists!")
            # Promote to admin if they exist
            existing_user.is_admin = True
            db.commit()
            print("Existing user promoted to admin.")
            return

        # Create new admin user
        admin_user = User(
            email=email,
            name=name,
            hashed_password=get_password_hashed(password),
            is_verified=True,
            is_admin=True,
            is_active=True
        )
        db.add(admin_user)
        db.commit()
        print(f"Superuser {email} created successfully!")

if __name__ == "__main__":
    create_superuser()