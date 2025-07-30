import os

# Load environment variables before using them
from src.utils.env_utils import load_dotenv_file

load_dotenv_file()


class WebUrls:
    """
    This class contains constants for web URLs used in the application.
    """

    # Base URL for the application
    BASE_URL = os.getenv("BASE_URL")
    GET_ALL_POST_URL = f"{BASE_URL}/author/{{author_id}}"


class SearchApis:
    SEARCH_API_URL = f"{WebUrls.BASE_URL}/?s={{query}}"
    GET_RELATED_POSTS_URL = f"{{POST_URL}}?relatedposts=1"


class ApiUrls:
    SEARCH = SearchApis()
