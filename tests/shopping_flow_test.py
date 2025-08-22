# tests/basic_UI_tests.py
import pytest
from pages.shop_page import ShoppingPage
from playwright.sync_api import expect
from pages.shop_page import ShoppingPage
from pages.sections.cart_section import CartSection
from pages.sections.product_list_section import ProductSection
import math

@pytest.mark.usefixtures("network_logger")  # Optional network logging
@pytest.mark.smoke
def test_shopping_flow_happy_path(page, network_logger):
    """
    Test basic shopping flow on the shopping page.
    Filter Produccts to Extra Small size
    Select first product
    Add to cart
    Verify cart updates correctly
    """
    shopping_page = ShoppingPage(page)
    
    # Navigate to shopping page
    shopping_page.goto("https://automated-test-evaluation.web.app/")
    shopping_page.verify_page_loaded()
    # Make Sure All Elements Are Visible
    shopping_page.logger.info("Checking visibility of all elements on the page")

    # --- Verify page is loaded with an empty cart ---
 
    expect(shopping_page.cart_quantity).to_be_visible()
    expect(shopping_page.cart_quantity).to_have_text("0") #expecting no items in cart at start of test

    #filter products to small size
    shopping_page.product_list_section.select_size("XS")
    #verify products are filtered to a single product
    expect(shopping_page.product_list_section.product_cards).to_have_count(1)
    #get product details for verification later
    product_list_product = shopping_page.product_list_section.get_all_products()[0]
    shopping_page.logger.info(f"Selected product: {product_list_product}")
    #add first product to cart
    shopping_page.product_list_section.click_add_to_cart(0) #click add to cart on first product
    #verify cart updates to 1 item
    expect(shopping_page.cart_quantity).to_have_text("1")
    #open the cart sideboard
    shopping_page.cart_section.open_cart()
    # Verify cart has 1 item
    expect(shopping_page.cart_section.cart_items).to_have_count(1)
    #verify cart item details match the product added
    cart_item = shopping_page.cart_section.get_cart_item(0)
    shopping_page.logger.info(f"Cart item: {cart_item}")
    assert cart_item.title == product_list_product.title
    product_price = float(product_list_product.price.replace("$", ""))
    assert cart_item.price == product_price, f"Expected price {product_price}, got {cart_item.price}"
    assert cart_item.quantity == 1, f"Expected quantity 1, got {cart_item.quantity}"
    # Verify checkout button is visible
    expect(shopping_page.cart_section.checkout_button).to_be_visible()
    # Verify quantity is 1
    assert cart_item.quantity == 1, f"Expected quantity 1, got {cart_item.quantity}"
    # Verify total price is correct
    expected_total = product_price * cart_item.quantity
    actual_total = shopping_page.cart_section.get_total_price()
    assert math.isclose(actual_total, expected_total, rel_tol=1e-9), f"Expected total {expected_total}, but got {actual_total}"
    #check out and inspect popup
    # --- Checkout and verify alert message ---
    # Trigger checkout and capture alert
    alert_message = shopping_page.cart_section.click_checkout(capture_alert=True)

    # Calculate expected total
    expected_total = product_price * cart_item.quantity

    # Format the expected alert string to match the actual alert
    total_str = f"$ {round(expected_total + 1e-8, 2):.2f}"  # space after $

    expected_alert_text = f"Checkout - Subtotal: {total_str}"
    assert expected_alert_text in alert_message, f"Unexpected alert text: {alert_message}"
    
    # Optional: inspect captured network requests
    if network_logger:
        shopping_page.logger.info(f"Captured {len(network_logger)} network requests")    
    
    # Capture error message, if any
    error_text = shopping_page.get_error_message()

    # Log the captured text for debugging
    shopping_page.logger.info(f"Captured error message: {error_text!r}")

    # Assert that no error message is present
    assert not error_text, f"Unexpected error message found: {error_text}"
