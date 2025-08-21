##Product List Section refers to the parts of the page inside the container than includes all product cards, size filters and 'star' repo link


from dataclasses import dataclass
from typing import List, Optional
from playwright.sync_api import Page, Locator
import re

@dataclass
class Product:
    title: str
    price: str
    shipping: str
    images: List[str]   # new field



class ProductSection:
    def __init__(self, page: Page):
        self.page = page
        # Section root: container holding all product cards
        self.root: Locator = page.locator("main.sc-ebmerl-3.hewZDo >> div.sc-uhudcz-0.iZZGui")
        # Locator for all product cards inside the section
        self.product_cards: Locator = self.root.locator("div.sc-124al1g-2")
        # Locator for the size filter container
        self.size_filter_container: Locator = page.locator("h4:has-text('Sizes:')").locator("..")  # parent div
 

    # --- Product methods ---

    #count of products in the section currently
    def count_products(self) -> int:
        return self.product_cards.count()
    
    #Get a specific product card by index
    def get_product_card(self, index: int) -> Locator:
        """Return a locator for the product card at the given index."""
        return self.product_cards.nth(index)
    
    # Get product details for a specific index
    def get_product_title(self, index: int) -> str:
        return self.product_cards.nth(index).locator("p.sc-124al1g-4").inner_text()

    # Get the price of a product at a specific index
    def get_product_price(self, index: int) -> str:
        card = self.product_cards.nth(index)
        small = card.locator("p.sc-124al1g-6 small").inner_text()
        main = card.locator("p.sc-124al1g-6 b").inner_text()
        fraction = card.locator("p.sc-124al1g-6 span").inner_text()
        return f"{small}{main}{fraction}"
    
    #add a product to the cart by index
    def get_product_shipping(self, index: int) -> str:
        return self.get_product_card(index).locator("div.sc-124al1g-3").inner_text()
    
    #get product images by index
    def get_product_images(self, index: int) -> List[Locator]:
        """Return a list of image locators for the product at the given index."""
        card = self.get_product_card(index)
        return [
            card.locator("img.sc-124al1g-0"),
            card.locator("img.sc-124al1g-1")
        ]

     # --- Create Structured Data List of all displayed products based on dataclass defined above ---
def get_all_products(self) -> list[Product]:
    """Return all products as structured Product objects with images."""
    products = []

    for i in range(self.count_products()):
        card = self.get_product_card(i)

        # --- Title ---
        title = card.locator("p.sc-124al1g-4").inner_text()

        # --- Price ---
        small = card.locator("p.sc-124al1g-6 small").inner_text()
        main = card.locator("p.sc-124al1g-6 b").inner_text()
        fraction = card.locator("p.sc-124al1g-6 span").inner_text()
        price = f"{small}{main}{fraction}"

        # --- Shipping ---
        shipping = card.locator("div.sc-124al1g-3").inner_text()

        # --- Images ---
        images = []
        image_container = card.locator("div.sc-124al1g-1")  # adjust selector as needed
        
        # Helper to extract URL from CSS background-image
        def extract_url(bg_value: str) -> str | None:
            if bg_value and bg_value != "none":
                match = re.search(r'url\(["\']?(.*?)["\']?\)', bg_value)
                if match:
                    return match.group(1)
            return None


        # Try to get the first image
        # CSS background-image extraction
        # This assumes the first image is set as a background image on the card element
        bg_image = image_container.evaluate(
            "el => window.getComputedStyle(el).backgroundImage"
        )
        print(f"[DEBUG] Card {i} default bg_image: {bg_image}")

        url1 = extract_url(bg_image)
        if url1:
            images.append(url1)

        # Try to get the second image
        #mouseover to enable 2nd image extraction
        image_container.hover()  # Ensure the second image is visible
        # CSS background-image extraction for the second image
        image_container.hover()
        bg_image2 = image_container.evaluate(
            "el => window.getComputedStyle(el).backgroundImage"
        )
        print(f"[DEBUG] Card {i} hover bg_image: {bg_image2}")

        url2 = extract_url(bg_image2)
        if url2 and url2 not in images:
            images.append(url2)


        # --- Build Product object ---
        products.append(Product(
            title=title,
            price=price,
            shipping=shipping,
            images=images
        ))

    return products

    # --- Size filter methods to interact with the UI size filter buttons---
    def select_size(self, size: str):
        checkbox = self.size_filter_container.locator(f"input[data-testid='checkbox'][value='{size}']")
        if not checkbox.is_checked():
            checkbox.check()

    def deselect_size(self, size: str):
        checkbox = self.size_filter_container.locator(f"input[data-testid='checkbox'][value='{size}']")
        if checkbox.is_checked():
            checkbox.uncheck()

    def deselect_all_sizes(self):
        checkboxes = self.size_filter_container.locator("input[data-testid='checkbox']")
        for i in range(checkboxes.count()):
            cb = checkboxes.nth(i)
            if cb.is_checked():
                cb.uncheck()

    def get_selected_sizes(self) -> list[str]:
        selected = []
        checkboxes = self.size_filter_container.locator("input[data-testid='checkbox']")
        for i in range(checkboxes.count()):
            cb = checkboxes.nth(i)
            if cb.is_checked():
                selected.append(cb.get_attribute("value"))
        return selected

    def deselect_all_sizes(self):
        checkboxes = self.size_filter_container.locator("input[data-testid='checkbox']")
        for i in range(checkboxes.count()):
            cb = checkboxes.nth(i)
            if cb.is_checked():
                cb.uncheck()

    def deselect_all_sizes(self):
        checkboxes = self.size_filter_container.locator("input[data-testid='checkbox']")
        for i in range(checkboxes.count()):
            cb = checkboxes.nth(i)
            if cb.is_checked():
                cb.uncheck()


 # ------------------------
    # Filter products in structured data list based on size, price, and title, without UI interaction, to be used for 
    # generating data subsets in later testing steps to compare with data generated via UI interactions
    # ------------------------
    @staticmethod
    def filter_by_min_price(products: List[Product], min_price: float) -> List[Product]:
        """Return products with price >= min_price."""
        result = []
        for p in products:
            price_value = float(p.price.replace("$", ""))
            if price_value >= min_price:
                result.append(p)
        return result

    @staticmethod
    def filter_by_max_price(products: List[Product], max_price: float) -> List[Product]:
        """Return products with price <= max_price."""
        result = []
        for p in products:
            price_value = float(p.price.replace("$", ""))
            if price_value <= max_price:
                result.append(p)
        return result

    @staticmethod
    def filter_by_price_range(products: List[Product], min_price: float, max_price: float) -> List[Product]:
        """Return products within a price range [min_price, max_price]."""
        result = []
        for p in products:
            price_value = float(p.price.replace("$", ""))
            if min_price <= price_value <= max_price:
                result.append(p)
        return result

    @staticmethod
    def filter_by_title_keyword(products: List[Product], keyword: str) -> List[Product]:
        """Return products where the title contains the given keyword (case-insensitive)."""
        keyword_lower = keyword.lower()
        return [p for p in products if keyword_lower in p.title.lower()]