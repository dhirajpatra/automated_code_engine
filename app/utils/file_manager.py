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
    Extract and save code files based on the OpenAI response.
    """
    try:
        if not response.strip():
            log_to_file(log_file_path, "Response is empty. No files to generate.")
            return False

        # Step 1: Create folder structure
        create_folder_structure(base_folder, response, log_file_path)
        log_to_file(log_file_path, "\n\nFolder structure created.\n\nNow creating files...\n\n")

        # Step 2: Extract file contents
        sections = response.split('#### File Contents', 1)
        if len(sections) < 2:
            log_to_file(log_file_path, "No '#### File Contents' section found.")
            return False

        file_contents_section = sections[1].strip()

        # Step 3: Match file blocks using updated regex
        file_pattern = re.compile(
            r'\*\*([\w/]+\.py|requirements\.txt)\*\*\n```(?:python|plaintext)?\n(.*?)```',
            re.DOTALL
        )
        matches = file_pattern.findall(file_contents_section)

        if not matches:
            log_to_file(log_file_path, "No files found within the 'File Contents' section.")
            return False

        log_to_file(log_file_path, f"Files detected: {len(matches)}")

        # Step 4: Save matched files
        for match in matches:
            file_path = match[0]  # Extract file path (e.g., app/main.py)
            file_content = match[1].strip()  # Extract file content

            # Full path for the file
            full_file_path = os.path.join(base_folder, file_path)
            os.makedirs(os.path.dirname(full_file_path), exist_ok=True)

            # Write content to the file
            with open(full_file_path, 'w') as f:
                f.write(file_content)
                log_to_file(log_file_path, f"File created: {full_file_path}")

        return True

    except Exception as e:
        log_to_file(log_file_path, f"An error occurred: {e}")
        return False

    