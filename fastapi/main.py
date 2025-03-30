from fastapi import FastAPI
from app.schema import ChatRequest
from app.utils import *

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
@app.get("/")
def read_root():
    return {"response": "Hello, World!"}

@app.post("/chat-v1")
def chat(request: ChatRequest):    
    response = llm.invoke(request.message)
    return {"response": response}

@app.post("/chat")
def chat(request: ChatRequest):    
    # Create the input string using the prompt template
    input_string = prompt.format(context=request.context, question=request.message)
    
    # Pass the formatted string to the invoke method
    response = llm.invoke(input_string)
    
    return {"response": response}
