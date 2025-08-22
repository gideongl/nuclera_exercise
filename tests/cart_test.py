# tests/cart_test.py
import math
import pytest
from playwright.sync_api import expect
from pages.shop_page import ShoppingPage
from pages.sections.cart_section import CartProduct

@pytest.mark.usefixtures("network_logger")
@pytest.mark.cart
def test_cart_dynamic_flow(page, network_logger):
    """
    Fully dynamic cart test:
    - Filter products
    - Add multiple products
    - Update quantities
    - Remove some/all
    - Verify quantities, subtotal, and checkout
    """

    shopping_page = ShoppingPage(page)

    # Navigate and verify page
    shopping_page.goto("https://automated-test-evaluation.web.app/")
    shopping_page.verify_page_loaded()
    shopping_page.logger.info("Page loaded successfully")

    # Verify empty cart
    expect(shopping_page.cart_quantity).to_be_visible()
    expect(shopping_page.cart_quantity).to_have_text("0")

    # Filter products to small size
    shopping_page.product_list_section.select_size("S")
    products = shopping_page.product_list_section.get_all_products()
    expect(shopping_page.product_list_section.product_cards).to_have_count(len(products))
    shopping_page.logger.info(f"Filtered products: {products}")

    # Add all products to cart
    for index in range(len(products)):
        shopping_page.product_list_section.click_add_to_cart(index)

    # Open cart and verify
    shopping_page.cart_section.open_cart()
    cart_products = shopping_page.cart_section.get_all_cart_products()
    assert len(cart_products) == len(products), f"Expected {len(products)} items, got {len(cart_products)}"

    # Verify titles, prices, and initial quantities
    for cart_item, product in zip(cart_products, products):
        assert cart_item.title == product.title
        assert cart_item.price == float(product.price.replace("$", ""))
        assert cart_item.quantity == 1

    # Increase quantity of each product by 2
    for cart_item in cart_products:
        shopping_page.cart_section.increase_quantity(cart_item.title, 2)

    # Re-fetch cart and verify total quantity
    cart_products = shopping_page.cart_section.get_all_cart_products()
    total_quantity = sum(item.quantity for item in cart_products)
    expect(shopping_page.cart_quantity).to_have_text(str(total_quantity))

    # Dynamically remove 1 quantity from first product (if exists)
    if cart_products:
        shopping_page.cart_section.decrease_quantity(cart_products[0].title, 1)

    cart_products = shopping_page.cart_section.get_all_cart_products()
    total_quantity = sum(item.quantity for item in cart_products)
    expect(shopping_page.cart_quantity).to_have_text(str(total_quantity))

    # Dynamically remove all quantities of the second product (if exists)
    if len(cart_products) > 1:
        shopping_page.cart_section.remove_item(cart_products[1].title)

    cart_products = shopping_page.cart_section.get_all_cart_products()
    total_quantity = sum(item.quantity for item in cart_products)
    expect(shopping_page.cart_quantity).to_have_text(str(total_quantity))

    # Verify subtotal dynamically
    expected_total = sum(item.subtotal for item in cart_products)
    actual_total = shopping_page.cart_section.get_total_price()
    assert math.isclose(actual_total, expected_total, rel_tol=1e-9), f"Expected total {expected_total}, got {actual_total}"

    # Checkout button visible
    expect(shopping_page.cart_section.checkout_button).to_be_visible()

    # Checkout and verify alert
    alert_message = shopping_page.cart_section.click_checkout(capture_alert=True)
    total_str = f"$ {round(expected_total + 1e-8, 2):.2f}"
    expected_alert_text = f"Checkout - Subtotal: {total_str}"
    assert expected_alert_text in alert_message, f"Unexpected alert text: {alert_message}"

    # Optional: log network requests
    if network_logger:
        shopping_page.logger.info(f"Captured {len(network_logger)} network requests")

    # Assert no error messages
    error_text = shopping_page.get_error_message()
    shopping_page.logger.info(f"Captured error message: {error_text!r}")
    assert not error_text, f"Unexpected error message found: {error_text}"
