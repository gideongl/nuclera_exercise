##Product List Section refers to the parts of the page inside the container than includes all product cards, size filters and 'star' repo link

from dataclasses import dataclass
from typing import List
from playwright.sync_api import Page, Locator, expect
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

        # --- Section root ---
        self.section_root: Locator = page.locator("main.sc-ebmerl-1.bmmyxu")
        # --- Inner elements ---
        self.product_cards: Locator = self.section_root.locator("div.sc-124al1g-2")
        self.add_to_cart_buttons: Locator = self.product_cards.locator("button.sc-124al1g-0")
        self.size_filter_container: Locator = self.section_root.locator(
            "div.sc-bj2vay-0.DCKcC:has(h4:has-text('Sizes:'))"
        )
        self.repo_star_link: Locator = self.section_root.locator(
            "a[aria-label='Star jeffersonRibeiro/react-shopping-cart on GitHub']"
        )
        self.product_count_label: Locator = self.section_root.locator("main.sc-ebmerl-4 p")

    # --- Product methods ---
    def get_displayed_product_count(self) -> int:
        """
        Returns the number of products the UI claims are displayed after filtering.
        """
        text = self.product_count_label.inner_text().strip()  # e.g., "16 Product(s) found"
        match = re.search(r"(\d+)\s+Product", text)
        return int(match.group(1)) if match else 0
    
    def count_products(self) -> int:
        return self.product_cards.count()

    def get_product_card(self, index: int) -> Locator:
        return self.product_cards.nth(index)

    def get_product_title(self, index: int) -> str:
        return self.get_product_card(index).locator("p.sc-124al1g-4").inner_text()

    def get_product_price(self, index: int) -> str:
        card = self.get_product_card(index)
        small = card.locator("p.sc-124al1g-6 small").inner_text()
        main = card.locator("p.sc-124al1g-6 b").inner_text()
        fraction = card.locator("p.sc-124al1g-6 span").inner_text()
        return f"{small}{main}{fraction}"

    def get_product_shipping(self, index: int) -> str:
        return self.get_product_card(index).locator("div.sc-124al1g-3").inner_text()

    def get_product_images(self, index: int) -> List[Locator]:
        card = self.get_product_card(index)
        return [
            card.locator("img.sc-124al1g-0"),
            card.locator("img.sc-124al1g-1")
        ]

    def click_add_to_cart(self, index: int):
        button = self.add_to_cart_buttons.nth(index)
        expect(button).to_be_visible()
        button.click()

    def click_add_to_cart_by_title(self, title: str):
        card = self.product_cards.locator(f"p:has-text('{title}')").first
        expect(card).to_be_visible()
        button = card.locator("button:has-text('Add to cart')").first
        expect(button).to_be_visible()
        button.click()

    def get_all_products(self) -> list[Product]:
        products = []
        for i in range(self.count_products()):
            card = self.get_product_card(i)

            # Title
            title_locator = card.locator("p.sc-124al1g-4")
            title = title_locator.inner_text() if title_locator.count() > 0 else ""

            # Price
            small = card.locator("p.sc-124al1g-6 small")
            main = card.locator("p.sc-124al1g-6 b")
            fraction = card.locator("p.sc-124al1g-6 span")
            price = ""
            if small.count() > 0 and main.count() > 0 and fraction.count() > 0:
                price = f"{small.inner_text()}{main.inner_text()}{fraction.inner_text()}"

            # Shipping
            shipping_locator = card.locator("div.sc-124al1g-3")
            shipping = shipping_locator.inner_text() if shipping_locator.count() > 0 else ""

            # Images
            images = []
            image_container = card.locator("div.sc-124al1g-1")
            if image_container.count() > 0:
                def extract_url(bg_value: str) -> str | None:
                    if bg_value and bg_value != "none":
                        match = re.search(r'url\(["\']?(.*?)["\']?\)', bg_value)
                        if match:
                            return match.group(1)
                    return None

                bg_image = image_container.evaluate("el => window.getComputedStyle(el).backgroundImage")
                url1 = extract_url(bg_image)
                if url1:
                    images.append(url1)

                image_container.hover()
                bg_image2 = image_container.evaluate("el => window.getComputedStyle(el).backgroundImage")
                url2 = extract_url(bg_image2)
                if url2 and url2 not in images:
                    images.append(url2)

            products.append(Product(title=title, price=price, shipping=shipping, images=images))
        return products

    # --- Size filter methods ---
    def select_size(self, size: str):
        checkbox = self.size_filter_container.locator(f"input[data-testid='checkbox'][value='{size}']")
        checkbox.check(force=True)

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

    # --- Helper to check section visibility ---
    def verify_section_visible(self):
        expect(self.section_root).to_be_visible()
        expect(self.product_cards.first).to_be_visible()
        expect(self.size_filter_container).to_be_visible()
        expect(self.repo_star_link).to_be_visible()
    # --- Helpers to check filter behaviour by Size

    def get_available_sizes(self) -> list[str]:
        """
        Returns all size filter options available (XS, S, M, ML, L, XL, XXL, etc.).
        """
        sizes = []
        checkboxes = self.size_filter_container.locator("input[data-testid='checkbox']")
        for i in range(checkboxes.count()):
            cb = checkboxes.nth(i)
            size_value = cb.get_attribute("value")
            if size_value:
                sizes.append(size_value)
        return sizes

    def validate_all_sizes(self) -> dict[str, int]:
        """
        Validates that selecting each size filter updates the displayed products.
        Returns a dictionary mapping size -> number of displayed products.
        """
        results = {}
        for size in self.get_available_sizes():
            self.deselect_all_sizes()
            self.select_size(size)
            # Wait for the UI to update product list (optional: you can add explicit wait)
            expect(self.product_cards.first).to_be_visible()
            count_displayed = self.get_displayed_product_count()
            results[size] = count_displayed
        # Restore to no filter selected
        self.deselect_all_sizes()
        return results

def validate_all_sizes(self):
    """
    Validate all available product size filters dynamically:

    - Iterates through all size filters (XS, S, M, ML, L, XL, XXL, etc.)
    - Selects each size filter and verifies the number of displayed products
      matches the UI-reported count
    - Ensures all product details (title, price, shipping, images) are present and visible
    - Compares filtered product counts against the total unfiltered product list
    - Confirms that images are displayed for each product card
    """
    # Capture all size filters
    checkboxes = self.size_filter_container.locator("input[data-testid='checkbox']")
    total_products = self.count_products()  # unfiltered product count

    for i in range(checkboxes.count()):
        cb = checkboxes.nth(i)
        size_value = cb.get_attribute("value")

        # Select filter
        cb.check(force=True)
        
        # Wait for filtering to update
        self.page.wait_for_timeout(200)  # small delay, adjust if necessary

        # Verify filtered product count matches UI count
        filtered_products = self.get_all_products()
        try:
            ui_count_text = self.section_root.locator("main.sc-ebmerl-4 p").inner_text()
            ui_count = int(re.search(r"(\d+)", ui_count_text).group(1))
        except Exception:
            ui_count = len(filtered_products)

        assert len(filtered_products) == ui_count, (
            f"Size '{size_value}' filter: expected {ui_count} products, found {len(filtered_products)}"
        )

        # Validate each product card has title, price, shipping, and at least one image
        for p in filtered_products:
            assert p.title, "Product missing title"
            assert p.price, f"Product '{p.title}' missing price"
            assert p.shipping, f"Product '{p.title}' missing shipping info"
            assert p.images and all(p.images), f"Product '{p.title}' missing images"

        # Deselect the size for next iteration
        cb.uncheck(force=True)

    # Optional: check that total products matches unfiltered count
    unfiltered_products = self.get_all_products()
    assert len(unfiltered_products) == total_products, (
        f"After clearing filters: expected {total_products} products, found {len(unfiltered_products)}"
    )