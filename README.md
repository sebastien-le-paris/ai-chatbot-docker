# AI Chatbot Docker

This document outlines the AI Chatbot Docker project, which integrates Ollama, FastAPI, Docker, and a Next.js frontend. The system is designed for deployment on local machines using Docker containers and includes the following features:

- Ollama for the LLM qwen2.5-coder:0.5b
- Langchain for the RAG
- FastAPI for the API
- Docker for containerization
- Next.js for the frontend
- TailwindCSS for styling
- Markdown rendering for responses
- Web UI for the chatbot
- File upload handling

## Setup Instructions

1. Clone the repository.
2. Execute `pdm install` to install the necessary dependencies.
3. Execute `pdm run dev` to initiate the development server.

## Implementation Details

### Ollama

Ollama serves as a lightweight, user-friendly, and efficient LLM server, ideal for local development and deployment.

- [Ollama on Docker Hub](https://hub.docker.com/search?q=ollama)
- [Ollama Library](https://ollama.com/library)
- [Ollama qwen2.5-coder:0.5b](https://ollama.com/library/qwen2.5-coder:0.5b)

To manage the Docker container, use the following commands:

- Start the container:
  ```
  $ docker compose up -d
  ```

- Stop the container:
  ```
  $ docker compose down
  ```

- Check the container status:
  ```
  $ docker ps -a
  ```

- View container logs:
  ```
  $ docker compose logs -f
  ```

- Rebuild and start the container:
  ```
  $ docker compose up -d --build
  ```

- View logs of the Ollama container:
  ```
  $ docker logs -f ollama-container
  ```

- Create a volume for the FastAPI container:
  ```
  $ docker volume create ollama-models
  ```

- Remove a volume:
  ```
  $ docker volume rm ollama-models
  ```

- Stop and remove volumes:
  ```
  $ docker compose down -v
  ```

### FastAPI

To set up the virtual environment and dependencies, execute the following commands:

- Create a virtual environment and activate it:
  ```
  $ python3.12 -m venv .venv
  $ source .venv/bin/activate
  ```

- Install the required dependencies:
  ```
  (.venv) $ pip install -r requirements.txt
  ```

- Run the FastAPI server:
  ```
  uvicorn main:app --reload
  ```

- Access the API documentation by navigating to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your web browser.

### GitHub

To commit and push changes to GitHub, follow these steps:

- Check the status of your repository:
  ```
  git status
  ```

- Stage all changes:
  ```
  git add .
  ```

- Commit the changes with a descriptive message:
  ```
  git commit -m "Updated chat function to format input for llm.invoke"
  ```

- Push the changes to the main branch or your specific branch:
  ```
  git push origin main  # or your branch name
  ```

### Frontend

To set up a new UI project using Next.js, Tailwind CSS, and Shadcn/UI, follow these steps:

1. Create a new Next.js project:
   ```
   cd frontend-app
   npx create-next-app@latest .
   ```

2. Navigate to the project directory:
   ```
   cd frontend-app
   ```

3. Install Tailwind CSS, shadcn/ui and its dependencies:
Initialize shadcn/ui:
https://ui.shadcn.com/docs/components/accordion
   ```
   npx shadcn@latest init
   ```

Add the components you need to the `components` folder.
   ```
   npx shadcn@latest add button input scroll-area textarea card
   ```

4. Initialize Tailwind CSS:
   ```
   npx tailwindcss init
   ```

   If you encounter the error "npm error could not determine executable to run", try the following steps to fix it:
   - Ensure you have the latest version of Node.js and npm installed.
   - Clear the npm cache by running:
     ```
     npm cache clean --force
     ```
   - Delete the `node_modules` folder and the `package-lock.json` file, then reinstall the dependencies:
     ```
     rm -rf node_modules package-lock.json
     npm install
     ```
   - Try running the Tailwind CSS initialization command again:
     ```
     npx tailwindcss init
     ```
     
Check for Global Installation Conflicts:
If you have a global installation of Tailwind CSS, it might conflict with the local installation. You can check for global installations with:
```
npm list -g --depth=0
```

If you find a global installation, you can remove it with:
```
npm uninstall -g tailwindcss
```

4. Configure Tailwind CSS by updating the `tailwind.config.js` file to include the paths to your template files.

5. Add Tailwind directives to your `styles/globals.css` file.

6. Install Shadcn/UI by following the instructions from their documentation.

7. Create a new folder for your components and add a chatbot component, e.g., `Chatbot.js`.

8. Import and use the Chatbot component in your `pages/index.js`.

9. Run your Next.js application:
   ```
   npm run dev
   ```

Your folder structure should resemble the following:

```
ui/
├── components/
│   └── Chatbot.js
├── pages/
│   └── index.js
├── public/
├── styles/
│   └── globals.css
├── tailwind.config.js
├── package.json
└── ...
```

### How to run the project

1. Start the Docker containers:
   ```
   docker compose up -d
   ```

Check the Docker containers are running:
```
docker ps -a
```

2. Start the FastAPI server:
   ```
   cd fastapi
   source .venv/bin/activate
   uvicorn main:app --reload
   ```

Check the FastAPI server is running:
```
curl http://127.0.0.1:8000/docs
```


3. Start the Next.js server:
  ```
   cd frontend-app
   npm run dev
   ```

4. Open your web browser and navigate to [http://localhost:3000](http://localhost:3000) to access the chatbot.

Check the Next.js server is running:
```
curl http://localhost:3000
```
