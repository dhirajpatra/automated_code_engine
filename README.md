
# Ollama, OpenAI Based Microservices Code Generation Engine Application

This application will generate code from prompt and front end code .dart

## Features
- It will generate back end fastapi based scripts from front end dart pages or swagger file of all APIs
- Model will be created
- Database will be created
- Microservices architecture with database and REST API based backend

## Prerequisites
- Docker
- Docker Compose
- Flask (for back-end)
- Front-end application framework (e.g., React)

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo/lcnc_code_engine.git
    cd lcnc_code_engine
    ```

2. **Build and run the Docker container:**
    ```bash
    sudo docker-compose up --build

    or
    
    docker-compose --env-file .env.dev up --build --remove-orphans

    ```

4. **Open the application:**
    - The FastAPI back-end will be running on port `8000`.

5. **Open Post man API testing**
    - Call the http://localhost:8000
    - call the POST http://localhost:8000/generate-backend/

6. **To Clean Docker Images**
    - `docker image rm $(docker images -f dangling=true)`

7. **If Issues Related to Folder and File Generation**
    - Check the log, openai response text and your regular expression in file_manager.py

Code Generator Engine will continue run as REST API server. It will have several APIs. Which will be called from workers running. Worker will read the messages from Rabbit MQ broker and call the API asynchronously. 

