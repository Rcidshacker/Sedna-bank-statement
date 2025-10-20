# --- Imports ---
import os
import uuid
from pathlib import Path
from fastapi import UploadFile

# --- Constants ---
# Define a directory to store temporary files.
# Using a subdirectory within the project makes it easy to manage and clean up.
TEMP_DIR = Path("temp_uploads")

# --- Core Function ---
def save_temp_file(file: UploadFile) -> str:
    """
    Saves an uploaded file to a temporary directory and returns its path.

    This function ensures that the temporary directory exists, generates a unique
    filename to prevent conflicts between simultaneous uploads, and saves the
    file content.

    Args:
        file (UploadFile): The file object received from the FastAPI endpoint.

    Returns:
        str: The absolute path to the saved temporary file.
    """
    
    # Step 1: Ensure the temporary directory exists.
    # The 'exist_ok=True' argument prevents an error if the directory
    # has already been created by a previous request.
    TEMP_DIR.mkdir(exist_ok=True)

    # Step 2: Generate a unique filename.
    # We combine a unique identifier (UUID) with the original file's extension.
    # This is a robust way to avoid filename collisions and security issues.
    # Example: 'my_statement.pdf' -> 'a1b2c3d4-e5f6-7890-1234-567890abcdef.pdf'
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    # Step 3: Define the full path for the new file.
    temp_file_path = TEMP_DIR / unique_filename

    # Step 4: Save the uploaded file's content to the new path.
    # We open the file in binary write mode ('wb') and write the content.
    # The 'await file.read()' asynchronously reads the content from the upload stream.
    try:
        with open(temp_file_path, "wb") as f:
            # Read the file content in chunks to handle large files efficiently
            while content := file.file.read(1024 * 1024): # Read in 1MB chunks
                f.write(content)
    finally:
        # Ensure the file pointer is reset, although it's less critical here
        # as we are done with the file object from the request.
        file.file.seek(0)

    # Step 5: Return the absolute path as a string.
    # The processing libraries will need this full path to access the file.
    return str(temp_file_path.resolve())