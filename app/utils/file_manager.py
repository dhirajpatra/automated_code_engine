# app/utils/file_manager.py
import os
import re
import shutil

def save_to_text_file(file_path, content):
    """Saves content to a text file."""
    with open(file_path, "w") as file:
        file.write(content)


def log_to_file(log_file_path: str, message: str):
    """Logs messages to a specified text file. This is a coroutine difficult to print on terminal."""
    with open(log_file_path, "a") as log_file:
        log_file.write(message + "\n")


def file_exists(file_path: str) -> bool:
    """
    Checks if the file already exists at the given path.
    """
    return os.path.isfile(file_path)


def create_folder_structure(base_folder: str, response: str, log_file_path: str):
    """
    Create the folder structure based on the response, deleting existing files and folders first.

    Args:
        base_folder (str): The base directory where folders will be created.
        response (str): The response string containing folder structure.
        log_file_path (str): Path to the log file where logs will be written.

    Returns:
        list: A list of created folder paths.
    """
    # Create the new base folder
    os.makedirs(base_folder, exist_ok=True)
    
    folder_paths = set()  # Use a set to avoid duplicates
    # Look for folder structure that starts with '###'
    folder_pattern = re.compile(r'### Folder Structure\n```(?:plaintext)?\n(.*?)\n```', re.DOTALL)
    folder_matches = folder_pattern.findall(response)

    if not folder_matches:
        log_to_file(log_file_path, "No folder structure found in response.")
        return folder_paths

    folder_structure = folder_matches[0]
    folder_lines = folder_structure.splitlines()

    for line in folder_lines:
        if '/' in line:
            folder_path = line.rstrip('/')
            full_folder_path = os.path.join(base_folder, folder_path)
            folder_paths.add(full_folder_path)

    for folder in folder_paths:
        os.makedirs(folder, exist_ok=True)
        log_to_file(log_file_path, f"Created folder: {folder}")

    return folder_paths


def extract_and_save_code(base_folder: str, response: str, log_file_path: str) -> bool:
    """
    Extract and save the code files based on the response in a two-step process:
    1. Extract the whole content from the ### File Contents section.
    2. Extract and save each specific file from its content.

    Args:
        base_folder (str): The base directory where folders will be created.
        response (str): The response string containing folder structure and file contents.
        log_file_path (str): Path to the log file where logs will be written.

    Returns:
        bool: True or False, indicating success or failure.
    """
    try:
        if not response.strip():
            log_to_file(log_file_path, "Response is empty. No files to generate.")
            return False
        
        # log_to_file(log_file_path, f"Response received: {response}")  # Debugging output
        create_folder_structure(base_folder, response, log_file_path)
        log_to_file(log_file_path, "\n\nFolder Structure created\n\nNow creating files in it\n\n")
        # log_to_file(log_file_path, f"Response received: {response}")

        # Step 1: Extract the whole content under ### File Contents
        patterns = [
            re.compile(r'### File Contents\n(.*?)(?=\n###|\Z)', re.DOTALL),
            re.compile(r'### Code Files\n(.*?)(?=\n###|\Z)', re.DOTALL),
            re.compile(r'(?i)(?:file|contents?):?\s*`([\w/]+\.py|requirements\.txt)`\s*```(?:python|plaintext)?\n(.*?)```', re.DOTALL),
            re.compile(r'File\s*([\w/]+\.py|requirements\.txt):?\n```(?:python|plaintext)?\n(.*?)```', re.DOTALL),
            re.compile(r'#### File: `([\w/]+\.py|requirements\.txt)`\n```(?:python|plaintext)?\n(.*?)```', re.DOTALL),
        ]

        matches = []
        for pattern in patterns:
            matches = pattern.findall(response)
            if matches:
                break  # Exit loop if matches found

        # # Step 1: Extract the whole content under ### File Contents
        # file_contents_pattern = re.compile(
        #     r'### File Contents\n(.*?)(?=\n###|\Z)', re.DOTALL
        # )
        # matches = file_contents_pattern.search(response)

        if not matches:
            log_to_file(log_file_path, "No file contents section found in the response.")
            return False

        file_contents = matches.group(1).strip()
        log_to_file(log_file_path, f"Extracted File Contents:\n{file_contents}")

        # Step 2: Extract each specific file and save it
        file_pattern = re.compile(
            r'#### ([\w/]+\.py|requirements\.txt)\n```(?:python|plaintext)?\n(.*?)```',
            re.DOTALL
        )

        matches = file_pattern.findall(file_contents)

        if not matches:
            log_to_file(log_file_path, "No files found within the File Contents section.")
            return False

        for match in matches:
            file_path = match[0]
            file_content = match[1].strip()
            full_file_path = os.path.join(base_folder, file_path)

            # Create parent directories if they don't exist
            os.makedirs(os.path.dirname(full_file_path), exist_ok=True)

            # Write the file content to the file
            with open(full_file_path, 'w+') as f:
                f.write(file_content)
                log_to_file(log_file_path, f"Written file: {full_file_path}")

        return True

    except Exception as e:
        log_to_file(log_file_path, f"An error occurred in extract_and_save_code: {e}")
        return False


    