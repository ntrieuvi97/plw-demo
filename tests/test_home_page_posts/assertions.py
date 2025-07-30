from src.page_objects.post_detail_page import PostDetailPage
from src.page_objects.home_page import HomePage


class HomePageAssertions:
    """
    Assertion helper class for home page test validations.

    This class provides methods to verify various states and behaviors
    of the home page, including post display and navigation functionality.

    Why?
        {Sometimes, we don't know how many check points we have placed in the test.
        This class centralizes assertions related to the home page.
        It helps in maintaining a clean separation of concerns,
        allowing tests to focus on behavior while assertions handle validation.
    """

    def __init__(self, page):
        self.home_page = HomePage(page)
        self.post_detail_page = PostDetailPage(page)

    def verify_that_all_posts_are_displayed(self, expected_count: int):
        """
        Verify that the exact number of posts are displayed on the home page.
        This method retrieves all visible posts from the home page and compares
        the count against the expected number. Fails with descriptive message
        if counts don't match.

        Why?
        {In user story, users expect to see a specific number of posts on the home page.
        They will see the posts listed, with titles, images, and dates.}

        Args:
            expected_count (int): The expected number of posts to be displayed.

        Raises:
            AssertionError: If the actual post count doesn't match expected count.

        Example:
            assertions.verify_that_all_posts_are_displayed(10)
        """
        actual_displayed_posts = [
            post for post in self.home_page.get_all_posts() if post.element.is_visible()
        ]

        assert (
            len(actual_displayed_posts) == expected_count
        ), f"Expected {expected_count} posts, but found {len(actual_displayed_posts)}."

        # Check that all posts have the required attributes
        for attr in ["title", "image_url", "created_date"]:
            assert all(
                hasattr(post, attr) for post in actual_displayed_posts
            ), f"Not all posts have a '{attr}' attribute."

    def verify_navigate_to_post_detail_successfully(self, expected_title: str):
        """
        Verify successful navigation to a post detail page with correct title.

        This method validates that after clicking on a post, the user is successfully
        navigated to the post detail page and the page displays the expected title.
        It performs an exact match comparison between expected and actual titles.

        Why?
        {In user story, users expect to click on a post and see its details.
        They will see the post title first, so it is crucial to ensure the title matches what was clicked.
        }

        Args:
            expected_title (str): The exact title expected to be displayed on the
                                post detail page.

        Raises:
            AssertionError: If the actual title doesn't exactly match the expected title.

        Note:
            This method assumes navigation has already occurred and validates the
            current state of the post detail page.

        Example:
            assertions.verify_navigate_to_post_detail_successfully("My Blog Post Title")
        """
        # Wait for navigation to complete
        actual_title = self.post_detail_page.get_post_title()
        print(f"Expected title: {expected_title}, Actual title: {actual_title}")

        # Verify the current URL matches the expected URI
        assert (
            expected_title == actual_title
        ), f"Expected title to contain '{expected_title}', but got '{actual_title}'."

    def verify_the_current_page_number(self, expected_number: int):
        """
        Verify that the current page number matches the expected page number.

        This method checks the pagination on the home page to ensure that the
        current page number is as expected. It raises an assertion error if
        the actual page number does not match the expected one.

        Why?
        {In user story, users expect to navigate through pages of posts.
        They will see the current page number in the pagination, so it is important to verify it.}

        Args:
            expected_number (int): The expected current page number.

        Raises:
            AssertionError: If the actual current page number does not match
                            the expected page number.

        Example:
            assertions.verify_the_current_page_number(2)
        """
        actual_page_number = self.home_page.get_current_page_number()
        assert (
            actual_page_number == expected_number
        ), f"Expected current page number to be {expected_number}, but got {actual_page_number}."
