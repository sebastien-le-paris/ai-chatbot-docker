from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field

# Define the ChatRequest model
class ChatRequest(BaseModel):
    message: str = Field(description="The message to send to the chatbot", 
                         default="How to implement fastapi router?")
    context: str = Field(description="The context to use for the chatbot", 
                         default="You are a helpful assistant that can answer questions in more details about the any frameworks for newbies and for non-tech people.")

class DataChat(SQLModel, table=True):
    __tablename__ = "datachat"  # Specify the table name explicitly
    id: int = Field(default=None, primary_key=True)
    message: str
    response: str
