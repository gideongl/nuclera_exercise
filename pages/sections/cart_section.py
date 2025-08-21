from playwright.sync_api import Page, expect
from dataclasses import dataclass
#dataclass for cart product details
@dataclass
class CartProduct:
    title: str
    quantity: int
    price: float  # single-item price
    subtotal: float  # quantity × price

##A POM for the section of the app that displays as a sideboard on the right side when opened and allows both inspection of the cart contents as well as the check-out action
class CartSection:
    def __init__(self, page: Page):
        self.page = page

        # Section root: container holding the entire cart section, starts from stable span 
        # name and goes up two levels of parents to the actual containing element with only a dynamic class name to link to, badly
        self.root = page.locator("span:has-text('Cart')").locator("..").locator("..")

        # Locators scoped to the section root
        self.cart_items = self.root.locator('.cart-item')
        self.checkout_button = self.root.locator("button:has-text('Checkout')")
        self.cart_quantity = self.root.locator("div[title='Products in cart quantity']")
        # Scoped checkout button locator under the existing section root
        self.checkout_button = self.root.locator("button:has-text('Checkout')")
        # --- Checkout button ---
        self.checkout_button = self.root.locator("button:has-text('Checkout')")

        # --- Quantity controls inside each cart item ---
        # These will be scoped per item as needed:
        #  - Minus button: disabled="" might be present
        #  - Plus button
        # Use per-item locators: item.locator("button:has-text('-')") etc.

        # --- Remove item button ---
        # Each remove button has title attribute
        self.remove_buttons = self.root.locator("button[title='remove product from cart']")

        # --- Cart close button ---
        # Assuming there is a visible "X" or close button somewhere in the header
        # Use the closest reliable element near the "Cart" text
        self.cart_close_button = self.root.locator("button:has-text('×'), span:has-text('×')")

        # --- Cart quantity display ---
        self.cart_quantity = self.root.locator("div[title='Products in cart quantity']")

    # --- Methods ---

    #get count of line items in the cart, not total quanitity of items to be purchased
    def get_cart_count(self) -> int:
        count_text = self.cart_quantity.inner_text()
        return int(count_text.strip())


#pop-up handler for checkout action
   # --- Click checkout and handle alert ---
    def click_checkout(self, capture_alert: bool = True) -> str | None:
        """Click checkout and capture the native alert message."""
        alert_message = None

        if capture_alert:
            def handle_dialog(dialog):
                nonlocal alert_message
                alert_message = dialog.message
                dialog.accept()

            self.page.on("dialog", handle_dialog)

        # Click the checkout button
        expect(self.checkout_button).to_be_visible()
        self.checkout_button.click()

        # Return the alert message for verification
        return alert_message
    
        # --- Close the cart side panel ---
    def close_cart(self):
        expect(self.cart_close_button).to_be_visible()
        self.cart_close_button.click()


# ---method to get structured cart product data ---
    def get_all_cart_products(self) -> list[CartProduct]:
        """Return all products in the cart as structured CartProduct objects."""
        products = []
        count = self.cart_items.count()
        for i in range(count):
            item = self.cart_items.nth(i)

            # --- Title ---
            title = item.locator("p.sc-11uohgb-2").inner_text().strip()

            # --- Quantity ---
            qty_text = item.locator("p.sc-11uohgb-3").inner_text().strip()  # e.g., "X | Wine \nQuantity: 1"
            # Extract number from "Quantity: 1"
            import re
            match = re.search(r"Quantity:\s*(\d+)", qty_text)
            quantity = int(match.group(1)) if match else 1

            # --- Price ---
            price_text = item.locator("div.sc-11uohgb-4 p").first.inner_text().strip()  # e.g., "$ 13.25"
            price = float(price_text.replace("$", "").strip())

            # --- Subtotal ---
            subtotal = price * quantity

            products.append(CartProduct(title=title, quantity=quantity, price=price, subtotal=subtotal))

        return products
    
     # --- Increase quantity for a specific item ---
    def increase_quantity(self, item_name: str, times: int = 1):
        item = self.cart_items.locator(f"p:has-text('{item_name}')").locator("..").locator("..")
        plus_button = item.locator("button:has-text('+')")
        for _ in range(times):
            expect(plus_button).to_be_enabled()
            plus_button.click()

    # --- Decrease quantity for a specific item ---
    def decrease_quantity(self, item_name: str, times: int = 1):
        item = self.cart_items.locator(f"p:has-text('{item_name}')").locator("..").locator("..")
        minus_button = item.locator("button:has-text('-')")
        for _ in range(times):
            if minus_button.is_enabled():
                minus_button.click()

    # --- Remove a specific item from the cart ---
    def remove_item(self, item_name: str):
        item = self.cart_items.locator(f"p:has-text('{item_name}')").locator("..").locator("..")
        remove_button = item.locator("button[title='remove product from cart']")
        expect(remove_button).to_be_visible()
        remove_button.click()

    # --- Verify an item exists in cart ---
    def verify_item_in_cart(self, item_name: str):
        item = self.cart_items.locator(f"p:has-text('{item_name}')")
        expect(item).to_be_visible()