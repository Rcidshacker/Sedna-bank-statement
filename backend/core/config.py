# --- Imports ---
from pydantic_settings import BaseSettings, SettingsConfigDict

# --- Configuration Class ---
class Settings(BaseSettings):
    """
    Manages the application's settings and environment variables.

    This class uses Pydantic's BaseSettings to automatically read variables
    from a .env file. This is a best practice for handling configuration
    and secrets without hardcoding them in the application.

    Attributes:
        OPENAI_API_KEY (str): The secret API key for accessing the OpenAI service.
                              It will be loaded from the .env file.
    """
    
    # Define the setting variable that needs to be loaded.
    # Pydantic will automatically look for an environment variable with this name.
    OPENAI_API_KEY: str

    # Configure Pydantic to look for a .env file in the project's root directory.
    # The .env file is where you will store your actual API key.
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# --- Instantiate Settings ---
# Create a single, global instance of the Settings class.
# Other parts of the application can import this 'settings' object
# to access configuration values easily.
settings = Settings()

# --- How to use this file ---
# 1. Create a file named '.env' in the root directory of your project
#    (the same level as the 'backend' and 'frontend' folders).
# 2. Inside the .env file, add the following line, replacing 'your_key_here'
#    with your actual OpenAI API key:
#
#    OPENAI_API_KEY="your_key_here"
#
# 3. The application will now automatically load this key when it starts.