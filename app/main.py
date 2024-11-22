# app/main.py
import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import models, schemas, database
from api.generate_backend import generate_backend_router  # Import the router


app = FastAPI()

# Configure the logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router for backend generation
app.include_router(generate_backend_router)

@app.on_event("startup")
async def startup_event():
    # Create the database tables when the app starts
    database.Base.metadata.create_all(bind=database.engine)

@app.get("/")
async def root():
    logger.info(f"*************** LCNC Code engine running ****************")
    return {"message": "FastAPI LCNC Backend is running"}
