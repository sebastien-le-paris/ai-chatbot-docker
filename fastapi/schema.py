from pydantic import BaseModel, Field
from typing import Optional, List
from sqlmodel import SQLModel, Field


# Define the ChatRequest model
class ChatRequest(BaseModel):
    message: str = Field(description="The message to send to the chatbot", 
                         default="How to implement fastapi router?")
    context: Optional[str] = Field(description="The context to use for the chatbot", 
                         default="You are a helpful assistant that can answer questions in more details about the any frameworks for newbies and for non-tech people.")


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

class ModelConfig(BaseModel):
    """Configuration model for LLM settings
    
    Attributes:
        model_name (str): Name of the LLM model to use
        temperature (float): Temperature setting for the model (0.0-1.0)
        max_tokens (int): Maximum number of tokens in the response
        base_url (str): URL of the Ollama server
    """
    model_name: str = Field(description="Name of the model to use", default="qwen2.5-coder:0.5b")
    temperature: float = Field(description="Temperature for the model (0.0-1.0)", default=0.7, ge=0.0, le=1.0)
    max_tokens: Optional[int] = Field(description="Maximum tokens in the response", default=None)
    base_url: str = Field(description="URL of the Ollama server", default="http://localhost:11434")

class ModelList(BaseModel):
    """List of available models
    
    Attributes:
        models (List[str]): List of available model names
    """
    models: List[str]
