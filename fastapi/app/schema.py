from pydantic import BaseModel, Field

# Define the ChatRequest model
class ChatRequest(BaseModel):
    message: str = Field(description="The message to send to the chatbot", 
                         default="How to implement fastapi router?")
    context: str = Field(description="The context to use for the chatbot", 
                         default="You are a helpful assistant that can answer questions about the any frameworks.")
