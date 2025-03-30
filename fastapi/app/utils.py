from operator import itemgetter
from typing import Any, Dict, List, Optional

from langchain.cache import InMemoryCache
from langchain.chains.llm import LLMChain
from langchain.globals import get_llm_cache, set_llm_cache
from langchain.sql_database import SQLDatabase
# from langchain.sql_database.query import create_sql_query_chain  
from langchain_community.tools import QuerySQLDataBaseTool
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from pydantic import BaseModel, Field

def get_embeddings():
    return OllamaEmbeddings(model="nomic-embed-text")

def get_llm():
    return OllamaLLM(model="qwen2.5-coder:0.5b")