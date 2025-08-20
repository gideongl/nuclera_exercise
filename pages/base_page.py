from playwright.sync_api import Page, Locator
from utils import wait
from utils.logger import get_logger

class BasePage:
    """Base class for all page objects with logging + wait wrappers."""

    def __init__(self, page: Page):
        self.page = page
        self.logger = get_logger(self.__class__.__name__)

    # ---------- Navigation ----------
    def goto(self, url: str):
        self.logger.info(f"Navigating to URL: {url}")
        self.page.goto(url)

    def current_url(self) -> str:
        return self.page.url

    # ---------- Wait helpers ----------
    def wait_for_visible(self, locator: Locator, timeout: float = 5000):
        self.logger.info(f"Waiting for element {locator} to be visible (timeout={timeout}ms)")
        wait.wait_for_element_visible(locator, timeout)

    def wait_for_hidden(self, locator: Locator, timeout: float = 5000):
        self.logger.info(f"Waiting for element {locator} to be hidden (timeout={timeout}ms)")
        wait.wait_for_element_hidden(locator, timeout)

    def wait_for_text(self, locator: Locator, text: str, timeout: float = 5000):
        self.logger.info(f"Waiting for text '{text}' in {locator} (timeout={timeout}ms)")
        wait.wait_for_text(locator, text, timeout)

    def wait_for_url_contains(self, fragment: str, timeout: float = 5000):
        self.logger.info(f"Waiting for URL to contain '{fragment}' (timeout={timeout}ms)")
        wait.wait_for_url(self.page, fragment, timeout)

    # ---------- Utility interactions ----------
    def click_and_wait(self, locator: Locator, url_fragment: str, timeout: float = 5000):
        self.logger.info(f"Clicking {locator} and waiting for URL to contain '{url_fragment}'")
        locator.click()
        self.wait_for_url_contains(url_fragment, timeout)

    def fill_and_log(self, locator: Locator, text: str):
        self.logger.info(f"Filling {locator} with text '{text}'")
        locator.fill(text)

    def get_text_and_log(self, locator: Locator) -> str:
        text = locator.text_content()
        self.logger.info(f"Extracted text from {locator}: '{text}'")
        return text

    def is_visible(self, locator: Locator) -> bool:
        visible = locator.is_visible()
        self.logger.info(f"Is {locator} visible? {visible}")
        return visible
