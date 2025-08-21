from playwright.sync_api import Page, expect

class ProductListSection:
    def __init__(self, page: Page):
        self.page = page
        self.product_cards = page.locator('.product-card')  # Example selector
        self.add_to_cart_buttons = page.locator('.product-card button.add-to-cart')
        
        #size filters locators
        self.size_xsize_xs_filter = page.locator("#password")
        self.size_size_s_filter = page.locator("#password")
        self.size_m_filter = page.locator("#password")
        self.size_ml_filter = page.locator("#password")
        self.size_l_filter = page.locator("#password")
        self.size_xl_filter = page.locator("#password")
        self.size_xxl_filter = page.locator("#password")

    def click_add_to_cart_for_product(self, product_name: str):
        product = self.page.locator(f'.product-card:has-text("{product_name}")')
        expect(product).to_be_visible()
        product.locator('button.add-to-cart').click()

    def verify_product_visible(self, product_name: str):
        product = self.page.locator(f'.product-card:has-text("{product_name}")')
        expect(product).to_be_visible()
