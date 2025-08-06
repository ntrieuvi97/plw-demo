import re
import unicodedata
from typing import Optional
from src.page_objects.post_detail_page import PostDetailPage
from src.page_objects.home_page import HomePage
from src.core.logger_controller import LoggerController


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

    def __init__(self, page, logger: Optional[LoggerController] = None):
        """
        Initialize assertions with page object and optional logger.

        Args:
            page: Playwright page object
            logger: Optional logger controller for detailed logging
        """
        self.home_page = HomePage(page)
        self.post_detail_page = PostDetailPage(page)
        self.logger = logger

    def _normalize_text(self, text: str) -> str:
        """Normalize Unicode text for consistent comparison with comprehensive cleaning."""
        if not text:
            return ""

        # Step 1: Unicode normalization (NFC)
        text = unicodedata.normalize("NFC", text)

        # Step 2: Remove invisible/control characters
        # Categories to remove: Cf (format), Cc (control), Cn (unassigned)
        text = "".join(
            char
            for char in text
            if unicodedata.category(char) not in ["Cf", "Cc", "Cn"]
        )

        # Step 3: Remove zero-width characters specifically
        zero_width_chars = [
            "\u200b",  # Zero Width Space
            "\u200c",  # Zero Width Non-Joiner
            "\u200d",  # Zero Width Joiner
            "\u2060",  # Word Joiner
            "\ufeff",  # Zero Width No-Break Space (BOM)
        ]
        for char in zero_width_chars:
            text = text.replace(char, "")

        # Step 4: Normalize whitespace
        text = re.sub(
            r"\s+", " ", text
        )  # Replace multiple whitespace with single space

        # Step 5: Strip leading/trailing whitespace
        return text.strip()

    def verify_displayed_posts_number(self, expected_count: int):
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

        actual_count = len(actual_displayed_posts)

        # Log the assertion result (with null check)
        if self.logger:
            self.logger.log_assertion(
                f"Expected {expected_count} posts, found {actual_count}",
                actual_count == expected_count,
            )

        assert (
            actual_count == expected_count
        ), f"Expected {expected_count} posts, but found {actual_count}."

        # Check that all posts have the required attributes
        for attr in ["title", "image_url", "created_date"]:
            attr_check_passed = all(
                hasattr(post, attr) for post in actual_displayed_posts
            )

            assert attr_check_passed, f"Not all posts have a '{attr}' attribute."

            # Log attribute check result (with null check)
            if self.logger:
                self.logger.log_assertion(
                    f"All posts have a '{attr}' attribute.",
                    attr_check_passed,
                )

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

        # Normalize both titles for comparison
        normalized_expected = self._normalize_text(expected_title)
        normalized_actual = self._normalize_text(actual_title)

        # Log assertion with null check
        if self.logger:
            self.logger.log_assertion(
                f"Expected post title: '{normalized_expected}', Actual post title: '{normalized_actual}'",
                normalized_expected == normalized_actual,
            )

        assert (
            normalized_expected == normalized_actual
        ), f"Expected title '{normalized_expected}', but got '{normalized_actual}'."

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

        # Log assertion with null check
        if self.logger:
            self.logger.log_assertion(
                f"Expected current page number: {expected_number}, Actual current page number: {actual_page_number}",
                actual_page_number == expected_number,
            )

        assert (
            actual_page_number == expected_number
        ), f"Expected current page number {expected_number}, but got {actual_page_number}."
