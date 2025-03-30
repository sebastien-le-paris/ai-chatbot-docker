from typing import Optional, Annotated  
from sqlmodel import create_engine, SQLModel, Session
from fastapi import Depends
from app.schema import DataChat  # Import DataChat from schema

DATABASE_URL = "sqlite:///./db.sqlite"  # Adjust your database URL as needed
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)  # This will create tables if they do not exist

def get_session():
    with Session(engine) as session:
        yield session

session_dependency = Annotated[Session, Depends(get_session)]

