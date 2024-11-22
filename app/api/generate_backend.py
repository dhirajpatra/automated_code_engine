# app/api/generate_backend.py
import os
from logger import logger
from fastapi import APIRouter, HTTPException
from utils import openai_langchain
from utils.file_manager import save_to_text_file
# from tasks import process_openai_response  # Ensure correct import
from tasks import process_openai_response

# Define the correct absolute directory for dart files and generated files
# dart_files_dir = os.path.join(os.getcwd(), 'dart_files')
swagger_files_dir = os.path.join(os.getcwd(), 'swagger_files')
generated_files_dir = os.path.join(os.getcwd(), 'generated_files')

generate_backend_router = APIRouter()

@generate_backend_router.post("/generate-backend/")
async def generate_backend():
    # Get the list of all .yaml files from the swagger_files folder
    if not os.path.exists(swagger_files_dir):
        raise HTTPException(status_code=400, detail="Swagger API yaml files directory not found.")

    swagger_files = [f for f in os.listdir(swagger_files_dir) if f.endswith('.yaml')]
    logger.info(f"Swagger files directory: {swagger_files_dir}")
    logger.info(f"Files found: {swagger_files}")
    
    if not swagger_files:
        logger.error("No swagger yaml files found")
        raise HTTPException(status_code=400, detail="No .yaml files found in the directory.")

    # Prepare content for OpenAI
    api_contents = []
    for yaml_file in swagger_files:
        with open(os.path.join(swagger_files_dir, yaml_file), 'r') as file:
            api_contents.append(file.read())

    swagger_files_combined = "\n\n".join(api_contents)
    escaped_swagger_files_combined = swagger_files_combined.replace("{", "{{").replace("}", "}}")

    # Create a comprehensive prompt for OpenAI
    prompt = (
        "Generate a Python FastAPI REST backend application from the provided Swagger API YAML content:\n"
        f"{escaped_swagger_files_combined}\n\n"
        "Requirements:\n"
        "- Start with the folder structure under the heading `### Folder Structure`.\n"
        "- Provide all file contents under the heading `#### File Contents` for each file.\n"
        "- Folder structure:\n"
        "  app/\n"
        "      __init__.py\n"
        "      main.py\n"
        "  models/\n"
        "      __init__.py\n"
        "      user.py (and additional model files as needed)\n"
        "  schemas/\n"
        "      __init__.py\n"
        "      user.py (and additional schema files as needed)\n"
        "  routes/\n"
        "      __init__.py\n"
        "      auth.py\n"
        "  database.py\n"
        "  requirements.txt\n\n"
        "- Implementation details:\n"
        "  - Use SQLAlchemy for database operations\n"
        "  - Use Pydantic for request and response validation\n"
        "  - Implement password hashing using bcrypt\n"
        "  - Handle user registration and login functionality in routes/auth.py\n"
        "  - Initialize FastAPI app in app/main.py\n"
        "  - Manage database connections and sessions in database.py\n"
        "  - Include necessary dependencies in requirements.txt\n"
        "  - Ensure the backend is fully functional and compatible with the FastAPI framework\n\n"
        "- Deliverables:\n"
        "  - Start with `### Folder Structure` for the folder structure.\n"
        "  - Provide all file contents under the heading `#### File Contents`.\n"
        "  - Fully functional code for the entire project folder structure.\n"
        "  - Complete files within the structure.\n"
        "  - Do not generate project root folder, instructions to run the application, explanations, or notes.\n"
    )
    
    try:
        # Call OpenAI to generate all necessary backend files
        generated_code_response = await openai_langchain.generate_code(prompt)

        # Create directories if they don't exist
        os.makedirs(os.path.dirname(generated_files_dir), exist_ok=True)

        # Save the OpenAI response to a text file for further processing
        openai_response_file = os.path.join(generated_files_dir, "openaiapi_response.txt")
        save_to_text_file(openai_response_file, generated_code_response.get('text'))

        # Call Celery task to process the response and generate the files
        process_openai_response.delay(generated_files_dir)  # Ensure this is correct
        # celery.send_task('tasks.process_openai_response', args=[generated_files_dir], kwargs={})

    except Exception as e:
        logger.error(f"Error generating files: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating files: {str(e)}")

    return {"message": "Backend code generated successfully and task initiated."}
