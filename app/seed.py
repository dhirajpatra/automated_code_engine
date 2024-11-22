from sqlalchemy.orm import Session
from database import SessionLocal
from models import User

# Seed data for users
def seed_users(db: Session):
    if db.query(User).count() == 0:
        print("Seeding users...")
        # Add a default user
        default_user = User(
            username="testuser",
            email="testuser@example.com",
            password="securepassword"  # In a real application, ensure to hash this password
        )
        db.add(default_user)
        db.commit()  # Commit the transaction
        print(f"User {default_user.email} added successfully!")
    else:
        print("Users table already seeded!")

def run_seeders():
    print("Running seeders...")
    db = SessionLocal()
    try:
        seed_users(db)
    except Exception as e:
        print(f"An error occurred while seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_seeders()
