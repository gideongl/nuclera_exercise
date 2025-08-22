# tests/product_list_test.py
import pytest
from pages.shop_page import ShoppingPage
from playwright.sync_api import expect
from pages.shop_page import ShoppingPage
from pages.sections.cart_section import CartSection
from pages.sections.product_list_section import ProductSection
import math

@pytest.mark.usefixtures("network_logger")  # Optional network logging
@pytest.mark.ui
def test_shopping_page_UI_check(page, network_logger):
    """
    Test basic navigatability and visibility of key elements on the shopping page across all sections
    """
    shopping_page = ShoppingPage(page)
    
    # Navigate to shopping page
    shopping_page.goto("https://automated-test-evaluation.web.app/")
    shopping_page.verify_page_loaded()
    # Make Sure All Elements Are Visible
    shopping_page.logger.info("Checking visibility of all elements on the page")

    # --- Verify main page locators are visible ---
    expect(shopping_page.repo_star_link).to_be_visible()
    expect(shopping_page.repo_cat_svg).to_be_visible()
    expect(shopping_page.cart_quantity).to_be_visible()
    expect(shopping_page.cart_quantity).to_have_text("0") #expecting no items in cart at start of test

    # --- Verify section elements are visible ---

    # Cart section checks
    #open the cart sideboard
    shopping_page.cart_quantity.click()
    # Verify cart section is visible
    shopping_page.cart_section.verify_section_visible()
    #close the cart sideboard, verification of it being open before and hidden after is implicit in the helper method used
    shopping_page.cart_section.close_cart()
    # Work Abroad section
    shopping_page.work_abroad_section.verify_section_visible()
    # Product list section
    shopping_page.product_list_section.verify_section_visible()
    
    # Optional: inspect captured network requests
    if network_logger:
        shopping_page.logger.info(f"Captured {len(network_logger)} network requests")    
    
    # Capture error message, if any
    error_text = shopping_page.get_error_message()

    # Log the captured text for debugging
    shopping_page.logger.info(f"Captured error message: {error_text!r}")

    # Assert that no error message is present
    assert not error_text, f"Unexpected error message found: {error_text}"


# ---- Section-specific tests ----

@pytest.mark.ui
def test_work_abroad_section(page):
    shopping_page = ShoppingPage(page)
    shopping_page.go_to_page("https://automated-test-evaluation.web.app/")

    section = shopping_page.work_abroad_section
    expect(section.section_root).to_be_visible()
    expect(section.heading).to_have_text("Work in the Netherlands")
    expect(section.linkedin_link).to_be_visible()


@pytest.mark.ui
def test_product_list_section(page):
    shopping_page = ShoppingPage(page)
    shopping_page.go_to_page("https://automated-test-evaluation.web.app/")

    section = shopping_page.product_list_section

    # Section root should be visible
    expect(section.section_root).to_be_visible()

    # At least one product card exists
    count = section.product_cards.count()
    assert count > 0, f"Expected at least one product card, but found {count}"

    # First product card's add-to-cart button is visible
    first_card = section.product_cards.first
    add_button = first_card.locator("button:has-text('Add to cart')")
    expect(add_button).to_be_visible()

    # Ensure get_all_products returns non-empty list
    products = section.get_all_products()
    assert products, "Expected non-empty list of products"


@pytest.mark.ui
def test_cart_section(page):
    shopping_page = ShoppingPage(page)
    shopping_page.go_to_page("https://automated-test-evaluation.web.app/")

    cart_section = CartSection(page, shopping_page)
    cart_section.open_cart()  # ensures the cart is visible

    expect(cart_section.section_root).to_be_visible()
    expect(cart_section.checkout_button).to_be_visible()