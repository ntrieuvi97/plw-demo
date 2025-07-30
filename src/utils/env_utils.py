import os
from dotenv import load_dotenv


def load_dotenv_file():
    """
    Load environment variables from a .env file.
    """
    # Load environment variables from .env file
    # You can set TARGET_ENV variable to 'dev', 'staging', or 'production'
    environment = os.getenv("TARGET_ENV", "dev")
    dotenv_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        ".env",
        f".env.{environment}",
    )
    load_dotenv(dotenv_path)
    
    return dotenv_path
