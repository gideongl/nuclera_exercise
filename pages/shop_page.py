from pages.base_page import BasePage
from pages.sections.work_abroad_section import WorkAbroadSection
from pages.sections.product_list_section import ProductListSection
from pages.sections.cart_section import CartSection
from playwright.sync_api import Page, expect

class ShoppingPage (BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.work_abroad_section = WorkAbroadSection(page)
        self.product_list_section = ProductListSection(page)
        self.cart_section = CartSection(page)
        
        #locators for the main page elements
        #locator for link to repo from the 'star' link in the midpage
        self.repo_star_link = page.locator('a[role="link"][aria-label="Star jeffersonRibeiro/react-shopping-cart on GitHub"]')
        #locator for the link to the repo from the octocat icon in the top left corner
        self.repo_cat_link = page.locator('a[aria-label="View source on Github"]')
        #cart sideboard locator for toggle to display sideboard
        self.cart_sideboard_toggle = page.locator("#username")
        #locator for page errors
        self.error_message_locator = page.locator(".error, .alert, [role='alert']")


    # Page-level methods
    def go_to_page(self, url: str):
        self.page.goto(url)

    # Method to get the page title and verify page has loaded
    def verify_page_loaded(self, expected_title: str = "Shopping Page"):
        assert self.get_title() == expected_title

    #Method to get any page error message
    def get_error_message(self) -> str:
        """Returns the text of the first visible error message, or None if none exist."""
        if self.error_message_locator.first.is_visible():
            return self.error_message_locator.first.inner_text().strip()
        return None