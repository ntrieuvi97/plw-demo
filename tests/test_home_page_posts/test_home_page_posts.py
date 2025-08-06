from playwright.sync_api import Page

from src.constants.test_configs import DeviceConstants, ScreenConstants
from src.page_objects.home_page import HomePage
from src.constants.urls import WebUrls
from random import choice

from src.core.decoration_controller import device_marker, screen_sizes


def test_verify_that_all_posts_are_displayed(
    page: Page, home_page: HomePage, assertions
):
    """
    Test to verify that all posts are displayed on the home page.
    Why?
        { This test ensures that the home page loads all posts correctly.
          It checks if the posts are displayed as expected, which is crucial for user experience. }
    Preconditions:
        - User is on the home page.
    Steps:
        1. Navigate to the home page.
        2. Scroll to the bottom to load all posts.
        3. Assert that all posts are displayed.
    Expected Result:
        - All posts should be displayed on the home page.
        - Title, image, and date of each post should be visible.
    """
    # Navigate to the home page
    page.goto(WebUrls.BASE_URL)
    # Scroll to the bottom to load all posts
    home_page.scroll_to_bottom()
    # Assert that all posts are displayed
    assertions.verify_displayed_posts_number(expected_count=10)


@device_marker(DeviceConstants.MOBILE.IPHONE_12)
def test_verify_that_user_can_view_the_post_details_by_clicking_on_title(
    page: Page, home_page: HomePage, assertions
):
    """
    Test to verify that a user can view the post details by clicking on a post.
    Why?
        { This test checks if clicking on a post title navigates the user to the post details page,
          ensuring that the navigation functionality works correctly. }

    Preconditions:
        - User is on the home page with posts displayed. They pick a random post.
    Steps:
        1. Navigate to the home page.
        2. Scroll to the bottom to load all posts.
        3. Click on a random post title.
        4. Assert that the post details page is displayed with the correct title.
    Expected Result:
        - The user should be able to view the post details page with the correct title.
    """
    # Set up: Navigate to the home page and pick a random post
    page.goto(WebUrls.BASE_URL)
    home_page.scroll_to_bottom()
    random_post = choice(home_page.get_all_posts())
    try:
        # Click on the post title to navigate to the post details page
        home_page.click_on_post_part(random_post, "title")

        # Assert that the post details page is displayed with the correct title
        assertions.verify_navigate_to_post_detail_successfully(
            expected_title=random_post.title
        )
    finally:
        # Tear down (if necessary)
        pass


@screen_sizes(ScreenConstants.FULL_HD)
def test_verify_that_user_can_view_the_post_details_by_clicking_on_image(
    page: Page, home_page: HomePage, assertions
):
    """
    Test to verify that a user can view the post details by clicking on the post image.
    Why?
        { This test checks if clicking on a post image navigates the user to the post details page,
        just imagine that you clicked on a post image and it does not do anything,
        it would be a bad user experience. }
    Preconditions:
        - The home page must be loaded, and posts must be displayed.
    Steps:
        1. Navigate to the home page.
        2. Scroll to the bottom to load all posts.
        3. Click on a random post image.
        4. Assert that the post details page is displayed with the correct title.
    Expected Result:
        - The user should be able to view the post details page with the correct title.
    """
    # Set up: Navigate to the home page and pick a random post
    page.goto(WebUrls.BASE_URL)
    home_page.scroll_to_bottom()
    random_post = choice(home_page.get_all_posts())
    try:
        # Click on the post image to navigate to the post details page
        home_page.click_on_post_part(random_post, "image")

        # Assert that all posts are displayed
        assertions.verify_navigate_to_post_detail_successfully(
            expected_title=random_post.title
        )
    finally:
        # Tear down (if necessary)
        pass


def test_verify_that_user_can_view_the_post_details_by_clicking_on_date(
    page: Page, home_page: HomePage, assertions
):
    """
    Test to verify that a user can view the post details by clicking on the post date.
    Why?
        { This test checks if clicking on a post date navigates the user to the post details page,
        this is a feature.}

    Preconditions:
        - User is on the home page with posts displayed. They pick a random post.

    Steps:
        1. Navigate to the home page.
        2. Scroll to the bottom to load all posts.
        3. Click on a random post date.
        4. Assert that the post details page is displayed with the correct title.

    Expected Result:
        - The user should be able to view the post details page with the correct title.
    """
    # Set up: Navigate to the home page and pick a random post
    page.goto(WebUrls.BASE_URL)
    home_page.scroll_to_bottom()
    random_post = choice(home_page.get_all_posts())
    try:
        # Click on the post date to navigate to the post details page
        home_page.click_on_post_part(random_post, "date")

        # Assert that all posts are displayed
        assertions.verify_navigate_to_post_detail_successfully(
            expected_title=random_post.title
        )
    finally:
        # Tear down (if necessary)
        pass
