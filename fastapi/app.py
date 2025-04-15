import requests
from fastapi import FastAPI, Response, Depends, HTTPException
from typing import Optional, AsyncGenerator
import os
from functools import lru_cache
from fastapi.responses import StreamingResponse
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
import asyncio

# Database
from db import (
    create_chat,
    get_all_chats,
    get_chat_by_id,
    delete_chat,
    DataChat,
    path_db,
    create_db_and_tables,
    session_dependency,
    DATABASE_URL
)
from sqlmodel import Session

# Langchain
from langchain_ollama import OllamaLLM # Ollama model
from langchain_ollama.llms import BaseLLM # Lớp cơ sở của LLM
from langchain.chains.llm import LLMChain # xử lí chuỗi các LLM
from langchain.chains.sql_database.query import create_sql_query_chain # tạo câu truy vấn cơ sở dữ liệu từ llm
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate # tạo câu truy vấn từ mẫu
from langchain_community.tools import QuerySQLDataBaseTool # công cụ truy vấn cơ sở dữ liệu
from langchain.sql_database import SQLDatabase # cơ sở dữ liệu
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser # xử lí kết quả trả về là kiểu dữ liệu chuỗi
from langchain_core.runnables import RunnablePassthrough # truyền đa dạng đối số
from operator import itemgetter # lấy giá trị từ dict

# Cache
from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache

# Schema
from schema import ChatRequest, ModelConfig, ModelList

# Utility
from utils import get_sql_from_answer_llm

app = FastAPI()

#test on docker
url_docker = "http://ollama-server:11434"
#test on local
url_local = "http://localhost:11434"
model = "qwen2.5-coder:0.5b"

llm = OllamaLLM(base_url=url_local, model="qwen2.5-coder:0.5b")

cache = InMemoryCache()
set_llm_cache(cache)

from db import DATABASE_URL
db = SQLDatabase.from_uri(DATABASE_URL)

template = """
{context}

Please answer the following question based on the context provided.

Question: {question}

Answer:
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | llm | StrOutputParser()

# Global model configuration
model_config = ModelConfig()

# Function to get the current LLM based on configuration
@lru_cache(maxsize=1)
def get_configured_llm():
    """
    Get the current LLM with configurations applied.
    
    Uses the global model_config to initialize an OllamaLLM instance.
    Results are cached until configuration changes.
    
    Returns:
        OllamaLLM: Configured language model instance
    """
    return OllamaLLM(
        base_url=model_config.base_url, 
        model=model_config.model_name,
        temperature=model_config.temperature,
        max_tokens=model_config.max_tokens
    )

@app.on_event("startup")
def connect_to_db():
    """
    Initialize database connection when the application starts.
    
    Creates necessary tables if they don't exist.
    """
    try:
        create_db_and_tables()  # Ensure this is only called once
    except Exception as e:
        # Handle the case where the table already exists or other errors
        print(f"Table creation skipped: {e}")

@app.get("/")
def read_root():
    """
    Root endpoint that returns a simple message.
    
    Returns:
        dict: Simple response indicating the API is functioning
    """
    return {"response": "Hello, World!"}

class StreamingResponseCallbackHandler(StreamingStdOutCallbackHandler):
    """Callback handler for streaming LLM responses"""
    
    def __init__(self):
        super().__init__()
        self.tokens = []
        self.queue = asyncio.Queue()

    def on_llm_new_token(self, token: str, **kwargs):
        self.tokens.append(token)
        if len(self.tokens) > 5:  # Buffer tokens for smoother streaming
            text = "".join(self.tokens)
            self.queue.put_nowait(text)
            self.tokens = []

    def on_llm_end(self, response, **kwargs):
        if self.tokens:  # Send any remaining tokens
            text = "".join(self.tokens)
            self.queue.put_nowait(text)
            self.tokens = []
        self.queue.put_nowait(None)  # Signal the end of streaming

@app.post("/ask")
def ask(chat_request: ChatRequest):
    """
    Process a chat request and return an AI response.
    
    Args:
        chat_request (ChatRequest): The chat request containing the message and optional context
        
    Returns:
        dict: Response containing the AI message and optional SQL results or errors
    """
    try:
        # Get the prompt from the request
        user_prompt = chat_request.message
        context = chat_request.context or ""
        
        # Get the configured LLM
        current_llm = get_configured_llm()
        
        # Invoke the language model
        res = current_llm.invoke({
            "tables": f"{db.get_table_info(db.get_usable_table_names())}",
            "context": context,
            "question": user_prompt
        })

        # Parse the response
        response = ""
        if isinstance(res, str):
            response = res
        elif isinstance(res, dict):
            response = res.get("message", str(res))
        else:
            response = str(res)

        # Save the response to the database 
        chat = create_chat(user_prompt, response)    

        # Try to extract SQL from the response and run it
        try:
            sql_query = get_sql_from_answer_llm(response)
            data_db = db.run(sql_query)
            return {
                "message": response,
                "chat_id": chat.id,
                "sql_query": sql_query,
                "sql_result": data_db
            }
        except Exception as sql_error:
            # SQL extraction or execution failed but we still return the LLM response
            return {
                "message": response,
                "chat_id": chat.id,
                "error": str(sql_error)
            }
    except Exception as e:
        # Handle general errors
        return {
            "error": f"Failed to process request: {str(e)}",
            "status_code": 500
        } 

@app.get("/chats", response_model=list[DataChat])
def get_chats():
    """Retrieve all chat history entries"""
    try:
        chats = get_all_chats()
        return chats
    except Exception as e:
        return {
            "error": f"Failed to retrieve chats: {str(e)}",
            "status_code": 500
        }

@app.get("/chats/{chat_id}", response_model=DataChat)
def get_chat(chat_id: int):
    """Retrieve a specific chat by ID"""
    try:
        chat = get_chat_by_id(chat_id)
        if chat:
            return chat
        return Response(content=f"Chat with ID {chat_id} not found", status_code=404)
    except Exception as e:
        return {
            "error": f"Failed to retrieve chat: {str(e)}",
            "status_code": 500
        }

@app.delete("/chats/{chat_id}")
def remove_chat(chat_id: int):
    """Delete a specific chat by ID"""
    try:
        deleted = delete_chat(chat_id)
        if deleted:
            return {"message": f"Chat with ID {chat_id} deleted successfully"}
        return Response(content=f"Chat with ID {chat_id} not found", status_code=404)
    except Exception as e:
        return {
            "error": f"Failed to delete chat: {str(e)}",
            "status_code": 500
        } 

@app.get("/models", response_model=ModelList)
def list_models():
    """List available models from Ollama server"""
    try:
        # Make a request to Ollama API to get models
        response = requests.get(f"{model_config.base_url}/api/tags")
        if response.status_code == 200:
            data = response.json()
            # Extract model names from the response
            models = [model["name"] for model in data.get("models", [])]
            return {"models": models}
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to retrieve models: {response.text}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to connect to Ollama server: {str(e)}"
        )

@app.post("/config", response_model=ModelConfig)
def update_model_config(config: ModelConfig):
    """Update the model configuration"""
    try:
        # Update the global model configuration
        global model_config
        model_config = config
        
        # Clear the LLM cache to force recreation with new config
        get_configured_llm.cache_clear()
        
        return model_config
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update configuration: {str(e)}"
        )

@app.get("/config", response_model=ModelConfig)
def get_model_config():
    """Get the current model configuration"""
    return model_config 

@app.post("/ask/stream")
async def ask_stream(chat_request: ChatRequest):
    """Stream the response for a chat request"""
    try:
        # Get the prompt from the request
        user_prompt = chat_request.message
        context = chat_request.context or ""
        
        # Set up the streaming callback
        callback_handler = StreamingResponseCallbackHandler()
        callback_manager = CallbackManager([callback_handler])
        
        # Get a streaming version of the LLM
        streaming_llm = OllamaLLM(
            base_url=model_config.base_url, 
            model=model_config.model_name,
            temperature=model_config.temperature,
            max_tokens=model_config.max_tokens,
            callback_manager=callback_manager
        )
        
        # Define the async generator for streaming
        async def stream_response() -> AsyncGenerator[str, None]:
            # Start the LLM invocation in a separate task
            asyncio.create_task(
                streaming_llm.ainvoke({
                    "tables": f"{db.get_table_info(db.get_usable_table_names())}",
                    "context": context,
                    "question": user_prompt
                })
            )
            
            # Yield tokens as they become available
            while True:
                token = await callback_handler.queue.get()
                if token is None:
                    break
                yield token
            
            # Save the complete response to the database
            complete_response = "".join(streaming_llm.generate_results)
            asyncio.create_task(
                asyncio.to_thread(create_chat, user_prompt, complete_response)
            )
        
        # Return the streaming response
        return StreamingResponse(
            stream_response(),
            media_type="text/plain"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process streaming request: {str(e)}"
        ) 

@app.get("/health")
def health_check():
    """Health check endpoint for container orchestration"""
    try:
        # Check database connectivity
        get_all_chats()
        
        # Check Ollama server connectivity
        response = requests.get(f"{model_config.base_url}/api/tags")
        if response.status_code != 200:
            return {
                "status": "unhealthy",
                "database": "healthy",
                "ollama_server": "unhealthy",
                "message": "Cannot connect to Ollama server"
            }
        
        return {
            "status": "healthy",
            "database": "healthy",
            "ollama_server": "healthy"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        } 