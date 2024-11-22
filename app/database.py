from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# Create the SQLAlchemy engine using the database URI from settings
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

# Create a declarative base class for your models
Base = declarative_base()

# Create a configured "SessionLocal" class
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

def get_db():
    """
    Dependency that provides a SQLAlchemy database session.
    
    Yields:
        Session: A SQLAlchemy session object.

    Ensures that the session is properly closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
