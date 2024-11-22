# app/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func  # Importing func here
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    # Relationship to GeneratedCode
    generated_codes = relationship("GeneratedCode", back_populates="user")

class GeneratedCode(Base):
    __tablename__ = 'generated_code'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    code = Column(Text)
    created_at = Column(TIMESTAMP, default=func.now())  # Now func is defined

    # Relationship to User
    user = relationship("User", back_populates="generated_codes")
