import os

class Settings:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:password123@pgsql/lcnc_db_dev")

settings = Settings()
