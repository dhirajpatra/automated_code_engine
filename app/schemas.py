# app/schemas.py
from pydantic import BaseModel, EmailStr, constr, Field
from typing import List, Optional

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=30, description="Username length constraints")
    email: EmailStr  # Valid email format

class UserCreate(UserBase):
    password: str = Field(..., description="The user's password")

class User(UserBase):
    id: int
    generated_codes: List['GeneratedCode'] = []  # Specify the type

    class Config:
        orm_mode = True

class GeneratedCodeBase(BaseModel):
    code: str

class GeneratedCodeCreate(GeneratedCodeBase):
    user_id: int

class GeneratedCode(GeneratedCodeBase):
    id: int
    created_at: str

    class Config:
        orm_mode = True
