from pages.base_page import BasePage
from pages.sections.work_abroad_section import WorkInNetherlandsSection
from pages.sections.product_list_section import ProductSection
from pages.sections.cart_section import CartSection
from playwright.sync_api import Page, expect

class ShoppingPage (BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.work_abroad_section = WorkInNetherlandsSection(page)
        self.product_list_section = ProductSection(page)
        self.cart_section = CartSection(page, self)

        #locators for the main page elements
        #locator for the link to the repo from the octocat icon in the top left corner
        self.repo_cat_link = page.locator("a[aria-label='View source on Github']")
        self.repo_cat_svg  = self.repo_cat_link.locator("svg")
        #Locator for 'star' repo link
        self.repo_star_link = page.locator('a[aria-label="Star jeffersonRibeiro/react-shopping-cart on GitHub"]')
        #cart sideboard locators 
        # Used for toggle to display sideboard and displaying the quantity of products in the cart displayed
         # Quantity element:
        # - Before: visible in the header (title attr version)
        # - After: inside the open cart section
        self.cart_quantity = page.locator(
            "div[title='Products in cart quantity'], div.sc-1h98xa9-3"
        )

        #locator for page errors
        self.error_message_locator = page.locator(".error, .alert, [role='alert']")


    #Return Page Title
    def get_title(self):
        return self.page.title()

    # Page-level methods
    def go_to_page(self, url: str):
        self.page.goto(url)

    # Method to get the page title and verify page has loaded
    def verify_page_loaded(self, expected_title: str = "Typescript React Shopping cart"):
        assert self.get_title() == expected_title

    #Method to get any page error message
    def get_error_message(self) -> str:
        """Returns the text of the first visible error message, or None if none exist."""
        if self.error_message_locator.first.is_visible():
            return self.error_message_locator.first.inner_text().strip()
        return None