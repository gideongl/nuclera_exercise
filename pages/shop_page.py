from pages.base_page import Basepage
from sections.work_abroad_section import WorkAbroadSection
from sections.product_list_section import ProductListSection
from sections.cart_section import CartSection
from playwright.sync_api import Page, expect

class ShoppingPage (Basepage):
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



    # Page-level methods
    def go_to_page(self, url: str):
        self.page.goto(url)

    def verify_page_loaded(self, title: str = "Shopping Page"):
        expect(self.page).to_have_title(title)