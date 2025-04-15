# AI SQL Chat API

A FastAPI application that integrates with Ollama LLMs to provide natural language querying over SQL databases. Ask questions in natural language, and the system will convert them to SQL queries and execute them against a database.

## Features

- **Natural Language to SQL**: Convert natural language questions into SQL queries
- **Chat History**: Store and retrieve chat history
- **Model Selection**: Switch between different language models
- **Streaming Responses**: Support for streaming responses for long-running queries
- **Configurable**: Adjust model parameters like temperature and token limits
- **Containerized**: Docker and docker-compose support for easy deployment

## Quick Start

### Using Docker Compose

The easiest way to get started is with Docker Compose:

```bash
# Clone the repository
git clone <repository-url>
cd <repository-directory>

# Start the application
docker-compose up --build

# The API will be available at http://localhost:8000
```

### Local Development

For local development:

```bash
# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r fastapi/requirements.txt

# Start the application
cd fastapi
uvicorn app:app --reload

# Make sure Ollama is running locally on port 11434
# Or update the configuration to point to your Ollama server
```

## API Documentation

Once the application is running, visit:
- http://localhost:8000/docs for the Swagger UI
- http://localhost:8000/redoc for the ReDoc UI

## Key Endpoints

- `POST /ask`: Submit a natural language query and get a response
- `POST /ask/stream`: Stream the response for a natural language query
- `GET /chats`: Get all chat history
- `GET /chats/{chat_id}`: Get a specific chat
- `DELETE /chats/{chat_id}`: Delete a specific chat
- `GET /models`: List available models
- `GET /config`: Get current model configuration
- `POST /config`: Update model configuration
- `GET /health`: Check service health

## Environment Variables

- `OLLAMA_BASE_URL`: URL of the Ollama server (default: http://localhost:11434)
- `MODEL_NAME`: Default model to use (default: qwen2.5-coder:0.5b)

## Technical Details

For detailed technical information, see the [Technical Design Document](docs/tdd.md).

## Task List

For implementation progress and upcoming tasks, see the [Task List](docs/task-list.md).
