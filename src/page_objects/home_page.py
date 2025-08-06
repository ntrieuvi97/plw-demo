from typing import List
from typing_extensions import Literal
from playwright.sync_api import Page

from src.constants.test_configs import ScrollConstants
from src.utils.scroll_utils import ScrollUtils
from .models.post_item import PostItem
from .post_detail_page import PostDetailPage


class HomePageLocators:
    """
    Class containing locators for the home page elements.
    This class is used to define the selectors for various elements on the home page.
    Why?
        { This class helps in maintaining the locators for the home page,
          making it easier to update and manage them in one place. }
    Why don't we move this to a separate file?
        { Keeping locators within the page object class allows for better encapsulation
          and easier maintenance, as the locators are closely tied to the behavior of the page.
          It also reduces the number of files in the project, making it more organized. }
    """

    POST_ITEMS_LOCATOR = "ul li.post"
    POST_TITLE_LOCATOR = ".wp-block-post-title a"
    POST_IMAGE_LOCATOR = ".wp-block-post-featured-image img"
    POST_DATE_LOCATOR = ".wp-block-post-date a"

    # Pagination locators
    PAGINATION_NUMBER_LOCATOR = "a:has-text('{page_number}')"
    PAGINATION_LOCATOR = ".wp-block-query-pagination-numbers"
    CURRENT_PAGE_LOCATOR = ".current"
    PREVIOUS_PAGE_LOCATOR = ".wp-block-query-pagination-previous span"
    NEXT_PAGE_LOCATOR = ".wp-block-query-pagination-next span"


class HomePage:

    def __init__(self, page: Page, logger=None):
        self.page = page
        self.locators = HomePageLocators()
        self.logger = logger

    def _extract_post_item(self, post_element) -> PostItem:
        """
        Extracts a PostItem from a post element.
        :param post_element: The element representing a post.
        :return: PostItem object containing title, image URL, created date, and the element itself.
        """
        """Extract PostItem from a post element."""
        title_el = post_element.query_selector(self.locators.POST_TITLE_LOCATOR)
        image_el = post_element.query_selector(self.locators.POST_IMAGE_LOCATOR)
        date_el = post_element.query_selector(self.locators.POST_DATE_LOCATOR)

        if not all([title_el, image_el, date_el]):
            return None

        return PostItem(
            title=title_el.inner_text().strip(),
            image_url=image_el.get_attribute("src"),
            created_date=date_el.inner_text().strip(),
            element=post_element,
        )

    def get_all_posts(self) -> List[PostItem]:
        """
        Retrieve all posts displayed on the home page.
        Returns a list of PostItem objects.
        """
        posts = self.page.query_selector_all(self.locators.POST_ITEMS_LOCATOR)
        post_items = []

        for post in posts:
            post_item = self._extract_post_item(post)
            if post_item:
                post_items.append(post_item)

        return post_items

    def click_on_post_part(
        self, post: PostItem, part: Literal["image", "title", "date"]
    ) -> PostDetailPage:
        """
        Click on a specific part (image, title, or date) of a post element.
        :param post: The PostItem object.
        :param part: The part to click on ('image', 'title', or 'date').
        :return: PostDetailPage instance after clicking.
        """
        locators = {
            "image": self.locators.POST_IMAGE_LOCATOR,
            "title": self.locators.POST_TITLE_LOCATOR,
            "date": self.locators.POST_DATE_LOCATOR,
        }
        if part not in locators:
            raise ValueError(
                f"Invalid part: {part}. Must be 'image', 'title', or 'date'."
            )
        target_post = post.element.query_selector(locators[part])
        if not target_post:
            raise RuntimeError(f"Could not find the {part} element in the post.")
        target_post.scroll_into_view_if_needed()
        target_post.click()

        return PostDetailPage(self.page)

    def scroll_to_bottom(self, scroll_count: int = ScrollConstants.SCROLL_STEP) -> None:
        """
        Scroll to the bottom of the page a specified number of times.
        Each scroll height is equal to the viewport height.
        :param scroll_count: Number of times to scroll down. Default is 10 times to ensure all posts are loaded.
        """
        ScrollUtils.scroll_to_bottom(self.page, scroll_count)
        return self

    def get_current_page_number(self) -> int:
        """
        Get the current page number from the pagination.
        Returns:
            int: The current page number.
        """
        try:
            current_page_element = self.page.locator(self.locators.CURRENT_PAGE_LOCATOR)
        except TimeoutError:
            return 1

        current_page_text = current_page_element.inner_text().strip()
        if not current_page_text:
            return 1

        return int(current_page_text)

    def click_on_page_navigation_number(self, page_number: int) -> "HomePage":
        """
        Click to navigate to a specific page in the pagination.
        :param page_number: The page number to navigate to.
        """
        pagination = self.page.locator(self.locators.PAGINATION_LOCATOR)
        target_page = pagination.locator(
            self.locators.PAGINATION_NUMBER_LOCATOR.format(page_number=page_number)
        )
        if target_page.is_visible():
            target_page.click()
            self.page.wait_for_load_state("load")
        return self

    def click_pagination_button(
        self, direction: Literal["next", "previous"]
    ) -> "HomePage":
        """
        Click to navigate to the next or previous page in the pagination.
        :param direction: 'next' or 'previous'
        """
        if direction not in ["next", "previous"]:
            raise ValueError("Direction must be 'next' or 'previous'.")

        locator = (
            self.locators.NEXT_PAGE_LOCATOR
            if direction == "next"
            else self.locators.PREVIOUS_PAGE_LOCATOR
        )
        direction_button = self.page.locator(locator)
        if direction_button.is_visible():
            direction_button.scroll_into_view_if_needed()
            direction_button.click()
            self.page.wait_for_load_state("load")
        return self
