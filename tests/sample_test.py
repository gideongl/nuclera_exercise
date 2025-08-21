# tests/test_login.py
import pytest
from pages.shop_page import ShoppingPage
from playwright.sync_api import expect

@pytest.mark.usefixtures("network_logger")  # Optional network logging
def test_shopping_page_UI_check(page, network_logger):
    """
    Test invalid login to verify:
    - Error message appears
    - Logs are captured
    - Screenshot taken on failure
    - Network requests logged
    """
    shopping_page = ShoppingPage(page)
    
    # Navigate to shopping page
    shopping_page.goto("https://automated-test-evaluation.web.app/")
    
    # Make Sure All Elements Are Visible
    shopping_page.logger.info("Checking visibility of all elements on the page")
    # --- Verify main page locators are visible ---
    expect(shopping_page.repo_star_link).to_be_visible()
    expect(shopping_page.repo_cat_link).to_be_visible()
    expect(shopping_page.cart_sideboard_toggle).to_be_visible()
    # --- Verify section elements are visible ---
    # Work Abroad section
    expect(shopping_page.work_abroad_section.section_root).to_be_visible()
    # Product list section
    expect(shopping_page.product_list_section.section_root).to_be_visible()
    # Cart section
    expect(shopping_page.cart_section.section_root).to_be_visible()



    # Optional: inspect captured network requests
    if network_logger:
        shopping_page.logger.info(f"Captured {len(network_logger)} network requests")    
    
    # Assert error message
    error_text = shopping_page.get_error_message()
    shopping_page.logger.info(f"Captured error message: {error_text}")
    assert error_text == "Not all expected elements are visible on the page", \
        f"Expected error message not found: {error_text}"   


# ---- Section-specific tests ----

@pytest.mark.ui
def test_work_abroad_section(page):
    shopping_page = ShoppingPage(page)
    shopping_page.go_to_page("https://react-shopping-cart-67954.firebaseapp.com/")

    section = shopping_page.work_abroad_section
    expect(section.section_root).to_be_visible()
    expect(section.heading).to_have_text("Work in the Netherlands")
    expect(section.linkedin_link).to_be_visible()


@pytest.mark.ui
def test_product_list_section(page):
    shopping_page = ShoppingPage(page)
    shopping_page.go_to_page("https://react-shopping-cart-67954.firebaseapp.com/")

    section = shopping_page.product_list_section
    expect(section.section_root).to_be_visible()
    expect(section.product_cards).to_have_count_greater_than(0)  # at least one product card
    expect(section.add_to_cart_buttons.first).to_be_visible()


@pytest.mark.ui
def test_cart_section(page):
    shopping_page = ShoppingPage(page)
    shopping_page.go_to_page("https://react-shopping-cart-67954.firebaseapp.com/")

    section = shopping_page.cart_section
    expect(section.section_root).to_be_visible()
    expect(section.checkout_button).to_be_visible()