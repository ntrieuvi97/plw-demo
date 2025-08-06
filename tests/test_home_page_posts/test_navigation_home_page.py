from time import sleep
from playwright.sync_api import Page

from src.page_objects.home_page import HomePage
from src.constants.urls import WebUrls


def test_verify_that_user_can_navigate_to_the_next_page_of_posts_by_clicking_number(
    page: Page, home_page: HomePage, assertions
):
    """
    Test to verify that a user can navigate to the next page of posts by clicking the next button.
    Why?
        { This test checks if the pagination functionality works correctly,
          allowing users to view more posts by navigating to the other pages. }

    Preconditions:
        - User is on the home page.
    Steps:
        1. Navigate to the home page.
        2. Click on the pagination number to go to the next page.
        3. Assert that the current page number is updated correctly.
    Expected Result:
        - The current page number should change to the next page number.
    """
    # Navigate to the home page
    page.goto(WebUrls.BASE_URL)

    try:
        # Click on the next button to navigate to the next page
        home_page.click_on_page_navigation_number(2)

        # Assert that the current URL has changed to the next page
        assertions.verify_the_current_page_number(2)

    finally:
        # Tear down (if necessary)
        pass


def test_verify_that_user_can_navigate_to_the_next_page_of_posts_by_clicking_next_button(
    page: Page, home_page: HomePage, assertions
):
    """
    Test to verify that a user can navigate to the next page of posts by clicking the next button.
    Why?
        { This test checks if the pagination functionality works correctly,
          allowing users to view more posts by navigating to the NEXT page. }
    Preconditions:
        - User is on the page which is not the first or last.
    Steps:
        1. Navigate to the page that is not the first or last.
        2. Click on the next button to go to the next page.
        3. Assert that the current page number is updated correctly.
    Expected Result:
        - The current page number should change to the next page number.
    """
    # Navigate to the home page
    page.goto(WebUrls.BASE_URL)
    home_page.click_on_page_navigation_number(2)

    try:
        # Click on the next button to navigate to the next page
        home_page.click_pagination_button("next")

        # Assert that the current URL has changed to the next page
        assertions.verify_the_current_page_number(3)

    finally:
        # Tear down (if necessary)
        pass


def test_verify_that_user_can_navigate_to_the_previous_page_of_posts_by_clicking_previous_button(
    page: Page, home_page: HomePage, assertions
):
    """
    Test to verify that a user can navigate to the previous page of posts by clicking the previous button.
    Why?
        { This test checks if the pagination functionality works correctly,
          allowing users to view more posts by navigating back to the previous page. }
    Preconditions:
        - User is on the page that is not the first or last.
    Steps:
        1. Navigate to the page that is not the first or last.
        2. Click on the previous button to go back to the previous page.
        3. Assert that the current page number is updated correctly.
    Expected Result:
        - The current page number should change to the previous page number.
    """
    # Navigate to the home page
    page.goto(WebUrls.BASE_URL)

    try:
        # Click on the next button to go to the second page first
        home_page.click_on_page_navigation_number(2)

        # Click on the previous button to navigate back to the first page
        home_page.click_pagination_button("previous")
        # Assert that the current URL has changed back to the first page
        assertions.verify_the_current_page_number(1)

    finally:
        # Tear down (if necessary)
        pass
