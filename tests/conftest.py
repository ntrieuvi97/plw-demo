import importlib
import pytest


@pytest.fixture
def pre_condition():
    pass


@pytest.fixture(autouse=True, scope="session")
def load_env():
    """
    Fixture to load environment variables before running tests.
    """
    from src.utils.env_utils import load_dotenv_file

    # Load environment variables from the appropriate .env file based on the ENVIRONMENT variable
    # This ensures that the environment is set up correctly for the tests.
    print("Loading environment variables...")
    dotenv_path = load_dotenv_file()
    print(f"Environment variables loaded from: {dotenv_path}")
    yield
