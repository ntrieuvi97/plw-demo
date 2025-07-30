from playwright.sync_api import Page
from src.constants.test_configs import ScrollConstants


class ScrollUtils:
    """Utility class for common scrolling operations across page objects.
    Why?
        {
            - Composition over Inheritance: More flexible and doesn't force a rigid class hierarchy
            - Single Responsibility: Each utility class has a focused purpose
            - Easier Testing: Static methods are easier to unit test
            - Less Coupling: Page objects aren't forced into an inheritance hierarchy
            - Extensibility: Easy to add more scroll utilities without affecting existing code
        }
    """

    @staticmethod
    def scroll_to_bottom(page: Page, scroll_count: int = 10, delay: int = None) -> None:
        """
        Scroll to the bottom of the page a specified number of times.
        Each scroll height is equal to the viewport height.

        Args:
            page: Playwright Page object
            scroll_count: Number of times to scroll down. Default is 10 times to ensure all posts are loaded.
            delay: Delay in milliseconds between scrolls. Uses ScrollConstants.SCROLL_DELAY if not provided.
        """
        delay = delay or ScrollConstants.SCROLL_DELAY
        for _ in range(scroll_count):
            page.evaluate("window.scrollBy(0, window.innerHeight)")
            page.wait_for_timeout(delay)

    @staticmethod
    def scroll_to_top(page: Page) -> None:
        """Scroll to the top of the page."""
        page.evaluate("window.scrollTo(0, 0)")

    @staticmethod
    def scroll_to_element(page: Page, selector: str) -> None:
        """
        Scroll to a specific element on the page.

        Args:
            page: Playwright Page object
            selector: CSS selector of the element to scroll to
        """
        element = page.locator(selector)
        element.scroll_into_view_if_needed()

    @staticmethod
    def scroll_by_pixels(page: Page, x: int = 0, y: int = 0) -> None:
        """
        Scroll by specific pixel amounts.

        Args:
            page: Playwright Page object
            x: Horizontal scroll amount in pixels
            y: Vertical scroll amount in pixels
        """
        page.evaluate(f"window.scrollBy({x}, {y})")

    @staticmethod
    def smooth_scroll_to_bottom(
        page: Page, scroll_count: int = 10, delay: int = None
    ) -> None:
        """
        Smoothly scroll to the bottom of the page with smaller increments.

        Args:
            page: Playwright Page object
            scroll_count: Number of scroll steps
            delay: Delay between scroll steps
        """
        delay = delay or ScrollConstants.SCROLL_DELAY
        viewport_height = page.evaluate("window.innerHeight")
        scroll_step = viewport_height // 4  # Scroll 1/4 of viewport height at a time

        for _ in range(scroll_count * 4):  # More steps for smoother scrolling
            page.evaluate(f"window.scrollBy(0, {scroll_step})")
            page.wait_for_timeout(delay // 4)
