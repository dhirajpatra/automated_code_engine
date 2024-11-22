# app/tasks.py
import os
from celery import Celery
from utils.file_manager import extract_and_save_code
from logger import create_logger

# Initialize logger
task_logger = create_logger("task_logger", "task.log")

# Initialize Celery with Redis
celery = Celery(
    'worker',
    broker='redis://redis:6379/0',  # Use Redis as broker
    backend='redis://redis:6379/0',   # Use Redis as backend
    include=["tasks"],
)

@celery.task(bind=True, time_limit=300, retry_backoff=True)  # 5-minute timeout
def process_openai_response(self, generated_files_dir):
    """
    Task to process and save OpenAI's response asynchronously.
    This function reads the response text from a file and extracts code from it.
    """
    # Define the log file path where logs will be saved
    log_file_path = os.path.join(generated_files_dir, "generation_logs.txt")

    if not isinstance(generated_files_dir, str) or not generated_files_dir.strip():
        raise ValueError("Invalid generated_files_dir in celery tasks")

    try:
        output_file_path = os.path.join(generated_files_dir, 'openaiapi_response.txt')
        with open(output_file_path, 'r') as file:
            response_text = file.read()
            
        # # Remove the file after reading
        # os.remove(output_file_path)
        
        task_logger.info("Processing OpenAI response from celery tasks. Calling file manager to extract and create folder with files in it ...")
        
        # Pass log_file_path to extract_and_save_code
        success = extract_and_save_code(generated_files_dir, response_text, log_file_path)

        if success:
            task_logger.info(f"Code generation completed. Logs saved to {log_file_path}")
        else:
            task_logger.error(f"Code generation failed. Check logs at {log_file_path}")
            
        return {"message": "Celery task complete"}

    except FileNotFoundError as e:
        task_logger.error(f"File not found in celery tasks: {output_file_path}")
        self.retry(exc=e, countdown=5, max_retries=3)
    except Exception as e:
        task_logger.error(f"Error in Celery task: {str(e)}")
        self.retry(exc=e, countdown=5, max_retries=3)

