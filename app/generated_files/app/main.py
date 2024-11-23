from fastapi import FastAPI
from routes.auth import router as auth_router
from database import engine
from models.user import Base

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Authentication API", description="API for user registration and login.", version="1.0.0")

app.include_router(auth_router)