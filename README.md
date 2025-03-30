# ai-chatbot-docker
AI Chatbot Docker

This chatbot is built with the help of Ollama, FastAPI, and Docker, and Next.js Frontend. This system is designed to be deployed on docker containers on local machine with the below features:

- Ollama for the LLM qwen2.5-coder:0.5b
- Langchain for the RAG
- FastAPI for the API
- Docker for containerization
- Next.js for the Frontend
- TailwindCSS for styling
- Markdown rendering for the responses
- Web UI for the chatbot
- File upload handling


## Setup

1. Clone the repository
2. Run `pdm install` to install the dependencies
3. Run `pdm run dev` to start the development server

## Implementation

### Ollama

Ollama is a lightweight, easy-to-use, and fast LLM server. It is a great tool for local development and deployment.

https://hub.docker.com/search?q=ollama

https://ollama.com/library

https://ollama.com/library/qwen2.5-coder:0.5b

Start the container
```
$ docker compose up -d
```

Stop the container
```
$ docker compose down
```

Check the container status
```
$ docker ps -a  
```

Check the logs of the container
```
$ docker compose logs -f
```

Rebuild and start the container
```
$ docker compose up -d --build
```

Check the logs of the ollama container
```
$ docker logs -f ollama-server
```

Check the logs of the fastapi container
```
$ docker logs -f fastapi
```

### FastAPI

Install virtual environment and dependencies
```
$ python3.12 -m venv .venv
$ source .venv/bin/activate
(.venv) $ pip install -r requirements.txt     
```

Run the FastAPI server
```     
uvicorn main:app --reload
```

Open the browser and navigate to http://127.0.0.1:8000/docs

### Github 

How to commit and push the changes to the github

``` 
git status
git add .
git commit -m "Updated chat function to format input for llm.invoke"
git push origin main  # or your branch name
```







