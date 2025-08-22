from __future__ import annotations  # allows forward references in type hints

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING
from playwright.sync_api import Page, expect

if TYPE_CHECKING:
    # only imported during type checking, avoids circular import
    from pages.shop_page import ShoppingPage


# dataclass for cart product details
@dataclass
class CartProduct:
    title: str
    quantity: int
    price: float  # single-item price
    subtotal: float  # quantity × price


class CartSection:
    def __init__(self, page: Page, shop_page: ShoppingPage) -> None:
        self.page = page
        self.shop_page = shop_page  # store reference to ShoppingPage

        # Section root
        self.section_root = page.locator("span:has-text('Cart')").locator("..").locator("..").locator("..")

        # Locators scoped to the section root
        self.cart_items = self.section_root.locator(".cart-item")
        self.checkout_button = self.section_root.locator("button:has-text('Checkout')")
        self.remove_buttons = self.section_root.locator("button[title='remove product from cart']")
        self.cart_close_button = self.section_root.locator("button:has-text('X')")

        # Cart quantity button is global (not inside section root)
        self.cart_quantity_button = page.locator("div[title='Products in cart quantity']")

    # --- Methods ---
    def open_cart(self) -> None:
        """Ensure the cart section is visible by clicking the cart quantity button from ShoppingPage if necessary."""
        if not self.section_root.is_visible():
            expect(self.shop_page.cart_quantity).to_be_visible()
            self.shop_page.cart_quantity.click()
            expect(self.section_root).to_be_visible()

    def get_cart_count(self) -> int:
        """Return the number of line items in the cart."""
        count_text = self.shop_page.cart_quantity.inner_text()
        return int(count_text.strip())

    def click_checkout(self, capture_alert: bool = True) -> str | None:
        """Click checkout and capture the native alert message."""
        alert_message = None

        if capture_alert:
            def handle_dialog(dialog):
                nonlocal alert_message
                alert_message = dialog.message
                dialog.accept()

            self.page.on("dialog", handle_dialog)

        expect(self.checkout_button).to_be_visible()
        self.checkout_button.click()

        return alert_message

    def close_cart(self) -> None:
        expect(self.cart_close_button).to_be_visible()
        self.cart_close_button.click()
        expect(self.section_root).to_be_hidden()

    def get_all_cart_products(self) -> list[CartProduct]:
        """Return all products in the cart as structured CartProduct objects."""
        products: list[CartProduct] = []
        count = self.cart_items.count()

        for i in range(count):
            item = self.cart_items.nth(i)

            title = item.locator("p.sc-11uohgb-2").inner_text().strip()

            qty_text = item.locator("p.sc-11uohgb-3").inner_text().strip()
            match = re.search(r"Quantity:\s*(\d+)", qty_text)
            quantity = int(match.group(1)) if match else 1

            price_text = item.locator("div.sc-11uohgb-4 p").first.inner_text().strip()
            price = float(price_text.replace("$", "").strip())

            subtotal = price * quantity

            products.append(CartProduct(title, quantity, price, subtotal))

        return products

    def increase_quantity(self, item_name: str, times: int = 1) -> None:
        item = self.cart_items.locator(f"p:has-text('{item_name}')").locator("..").locator("..")
        plus_button = item.locator("button:has-text('+')")
        for _ in range(times):
            expect(plus_button).to_be_enabled()
            plus_button.click()

    def decrease_quantity(self, item_name: str, times: int = 1) -> None:
        item = self.cart_items.locator(f"p:has-text('{item_name}')").locator("..").locator("..")
        minus_button = item.locator("button:has-text('-')")
        for _ in range(times):
            if minus_button.is_enabled():
                minus_button.click()

    def set_quantity(self, item_name: str, target_quantity: int) -> None:
        item = self.cart_items.locator(f"p:has-text('{item_name}')").locator("..").locator("..")
        qty_text = item.locator("p.sc-11uohgb-3").inner_text()
        match = re.search(r"Quantity:\s*(\d+)", qty_text)
        current_quantity = int(match.group(1)) if match else 0

        if current_quantity < target_quantity:
            plus_button = item.locator("button:has-text('+')")
            for _ in range(target_quantity - current_quantity):
                expect(plus_button).to_be_enabled()
                plus_button.click()
        elif current_quantity > target_quantity:
            minus_button = item.locator("button:has-text('-')")
            for _ in range(current_quantity - target_quantity):
                if minus_button.is_enabled():
                    minus_button.click()

    def remove_item(self, item_name: str) -> None:
        item = self.cart_items.locator(f"p:has-text('{item_name}')").locator("..").locator("..")
        remove_button = item.locator("button[title='remove product from cart']")
        expect(remove_button).to_be_visible()
        remove_button.click()

    def verify_item_in_cart(self, item_name: str) -> None:
        item = self.cart_items.locator(f"p:has-text('{item_name}')")
        expect(item).to_be_visible()
