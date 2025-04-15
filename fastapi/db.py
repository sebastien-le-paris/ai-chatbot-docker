from typing import Optional, Annotated  
from sqlmodel import (
    SQLModel,
    create_engine, 
    Session,
    select,
    Field
)
from fastapi import Depends

DATABASE_URL = "sqlite:///./db.sqlite"  # Adjust your database URL as needed
engine = create_engine(DATABASE_URL)

class DataChat(SQLModel, table=True):
    """Model for storing chat messages and responses in database
    
    Attributes:
        id (int): Primary key ID for the chat entry
        message (str): The user's input message 
        response (str): The response generated for the message
    """
    id: int | None = Field(default=None, primary_key=True, index=True)
    message: str
    response: str

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)  # This will create tables if they do not exist

def get_session():
    """Get a database session
    
    Yields:
        Session: Database session for executing queries
    """
    with Session(engine) as session:
        yield session

def create_chat(message: str, response: str):
    """Create a new chat entry in the database
    
    Args:
        message (str): The user's input message
        response (str): The generated response
        
    Returns:
        DataChat: The created chat entry
    """
    chat = DataChat(message=message, response=response)
    with Session(engine) as session:
        session.add(chat)
        session.commit()
        session.refresh(chat)
    return chat

def get_all_chats():
    """Get all chat entries from the database
    
    Returns:
        list[DataChat]: List of all chat entries
    """
    with Session(engine) as session:
        statement = select(DataChat)
        chats = session.exec(statement).all()
        return chats

def get_chat_by_id(chat_id: int):
    """Get a specific chat entry by ID
    
    Args:
        chat_id (int): ID of the chat to retrieve
        
    Returns:
        DataChat | None: The chat entry if found, None otherwise
    """
    with Session(engine) as session:
        statement = select(DataChat).where(DataChat.id == chat_id)
        chat = session.exec(statement).first()
        return chat

def delete_chat(chat_id: int):
    """Delete a chat entry from the database
    
    Args:
        chat_id (int): ID of the chat to delete
        
    Returns:
        bool: True if chat was deleted, False if not found
    """
    with Session(engine) as session:
        chat = get_chat_by_id(chat_id)
        if chat:
            session.delete(chat)
            session.commit()
            return True
        return False


session_dependency = Annotated[Session, Depends(get_session)]

