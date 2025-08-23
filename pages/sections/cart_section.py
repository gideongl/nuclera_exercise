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
    def __init__(self, page: Page, shop_page: "ShoppingPage") -> None:
        self.page = page
        self.shop_page = shop_page  # store reference to ShoppingPage

        # Section root (cart sidebar container)
        self.section_root = page.locator("div.sc-1h98xa9-4")

        # Cart items identified by having a Quantity: label
        # In CartSection __init__
        self.cart_items = self.section_root.locator("div.sc-11uohgb-0.hDmOrM")


        # Buttons & actions inside cart
        # Checkout button
        self.checkout_button = self.section_root.get_by_role("button", name="Checkout")
        # Remove product buttons
        self.remove_buttons = self.section_root.get_by_title("remove product from cart")
        self.cart_close_button = self.section_root.locator("button:has-text('X')")

        # Cart quantity button is global (outside section root)
        self.cart_quantity_button = page.locator("div[title='Products in cart quantity']")

        #locators for cart information
        self.total_price = self.section_root.locator("div.sc-1h98xa9-8.bciIxg > p.sc-1h98xa9-9.jzywDV")


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
    
    def get_cart_item(self, index: int) -> CartProduct:
        """Return the cart item at the given index as a structured object."""
        item = self.cart_items.nth(index)
        
        # Title
        title = item.locator("p.sc-11uohgb-2.elbkhN").inner_text()

        # Quantity
        quantity_text = item.locator("p.sc-11uohgb-3.gKtloF").inner_text()
        # extract number after "Quantity:"
        import re
        match = re.search(r"Quantity:\s*(\d+)", quantity_text)
        quantity = int(match.group(1)) if match else 1

        # Price per unit
        price_text = item.locator("div.sc-11uohgb-4.bnZqjD > p").inner_text()
        price = float(price_text.replace("$", "").strip())

        # Subtotal (price * quantity)
        subtotal = round(price * quantity, 2)

        return CartProduct(title=title, quantity=quantity, price=price, subtotal=subtotal)

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
    
    def get_total_price(self) -> float:
        """Return the cart total as a float."""
        text = self.total_price.inner_text().replace("$", "").strip()
        return float(text)

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


    #Ensure Empty Cart UI elements are displayed when sideboard is opened with no items in cart
    def verify_section_visible(self):
        """
        Assert that the cart section root and key inner elements are visible,
        handling animations and delayed rendering.
        """
        # Wait for the cart panel container
        cart_panel = self.page.locator("div.sc-1h98xa9-1.kQlqIC")
        cart_panel.wait_for(state="visible", timeout=5000)

        # Cart items
        if self.cart_items.count() > 0:
            expect(self.cart_items.first).to_be_visible(timeout=5000)

        # Checkout button
        expect(self.checkout_button).to_be_visible(timeout=5000)

        # Close button
        self.cart_close_button = cart_panel.locator("button:has-text('X')")
        self.cart_close_button.wait_for(state="visible", timeout=5000)
        expect(self.cart_close_button).to_be_visible()

