from playwright.sync_api import Page


class PostDetailPage:
    POST_TITLE_LOCATOR = "h1.wp-block-post-title"

    def __init__(self, page: Page):
        self.page = page

    def get_post_title(self) -> str:
        """
        Retrieve the title of the post from the post detail page.
        """
        return self.page.locator(self.POST_TITLE_LOCATOR).inner_text()
