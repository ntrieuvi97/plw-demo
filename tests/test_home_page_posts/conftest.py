import pytest
from playwright.sync_api import Page

from .assertions import HomePageAssertions
from src.page_objects.home_page import HomePage


@pytest.fixture
def assertions(page, logger_controller) -> HomePageAssertions:
    """
    Provide assertions helper with integrated logging.
    """
    logger = logger_controller
    return HomePageAssertions(page, logger)


@pytest.fixture()
def home_page(page: Page):
    """
    Fixture to initialize the HomePage object for tests.
    """

    yield HomePage(page)
