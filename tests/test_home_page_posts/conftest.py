import pytest
from playwright.sync_api import Page

from .assertions import HomePageAssertions
from src.page_objects.home_page import HomePage


@pytest.fixture()
def assertions(page):
    """
    Fixture to provide assertions for home page tests.
    """
    yield HomePageAssertions(page)


@pytest.fixture()
def home_page(page: Page):
    """
    Fixture to initialize the HomePage object for tests.
    """

    yield HomePage(page)
