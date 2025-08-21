from playwright.sync_api import Page, expect

class CartSection:
    def __init__(self, page: Page):
        self.page = page
        self.cart_items = page.locator('.cart-item')
        self.checkout_button = page.locator('button#checkout')
        self.cart_sideboard_close = page.locator("#username")
        self.cart_sideboard_checkout_button = page.locator("#username")
        self.checkout_popup = page.locator("#username")

    def verify_item_in_cart(self, item_name: str):
        item = self.page.locator(f'.cart-item:has-text("{item_name}")')
        expect(item).to_be_visible()

    def click_checkout(self):
        expect(self.checkout_button).to_be_visible()
        self.checkout_button.click()
