from dataclasses import dataclass
from playwright.sync_api import ElementHandle


@dataclass
class PostItem:
    title: str
    image_url: str = ""
    created_date: str = ""
    element: ElementHandle = None
    author: str = ""
    content: str = ""
