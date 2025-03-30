from fastapi import FastAPI, Depends
from app.schema import ChatRequest, DataChat
from app.utils import *
from app.db import create_db_and_tables, session_dependency
from sqlmodel import Session    

app = FastAPI()

llm = OllamaLLM(base_url="http://localhost:11434", model="qwen2.5-coder:0.5b")

cache = InMemoryCache()
set_llm_cache(cache)

template = """
{context}

Please answer the following question based on the context provided.

Question: {question}

Answer:
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | llm | StrOutputParser()

@app.on_event("startup")
def connect_to_db():
    try:
        create_db_and_tables()  # Ensure this is only called once
    except Exception as e:
        # Handle the case where the table already exists or other errors
        print(f"Table creation skipped: {e}")

@app.get("/")
def read_root():
    return {"response": "Hello, World!"}

@app.post("/chat-v1")
def chat(request: ChatRequest):    
    response = llm.invoke(request.message)
    return {"response": response}

@app.post("/chat")
def chat(request: ChatRequest, session: session_dependency):    
    # Create the input string using the prompt template
    input_string = prompt.format(context=request.context, question=request.message)
    
    # Pass the formatted string to the invoke method
    response = llm.invoke(input_string)

    session.add(DataChat(message=request.message, response=response))
    session.commit()
    
    return {"response": response}
