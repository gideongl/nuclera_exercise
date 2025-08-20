from playwright.sync_api import Page
from pages.base_page import BasePage

class RepoPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login")
        self.error_message = page.locator("#error")

    def login(self, username: str, password: str):
        self.fill_and_log(self.username_input, username)
        self.fill_and_log(self.password_input, password)
        self.click_and_wait(self.login_button, "dashboard")

    def get_error_message(self) -> str:
        return self.get_text_and_log(self.error_message)
