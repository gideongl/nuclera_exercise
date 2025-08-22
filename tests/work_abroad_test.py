# tests/work_abroad_test.py
import pytest
from pages.shop_page import ShoppingPage
from playwright.sync_api import expect
from pages.shop_page import ShoppingPage
from pages.sections.cart_section import CartSection
from pages.sections.product_list_section import ProductSection
import math

@pytest.mark.usefixtures("network_logger")  # Optional network logging
@pytest.mark.work_abroad
def test_work_abroad_section_and_link(page, network_logger):
    """
    Open App
    Check Work Abroad Section visibility
    Check Linked_In_link works
    """
    shopping_page = ShoppingPage(page)
    
    # Navigate to shopping page
    shopping_page.goto("https://automated-test-evaluation.web.app/")
    shopping_page.verify_page_loaded()

    # --- Verify a main page locator is visible ---
    expect(shopping_page.repo_star_link).to_be_visible()

    # --- Verify section elements are visible ---
    # Work Abroad section
    shopping_page.work_abroad_section.verify_section_visible()
    shopping_page.work_abroad_section.click_linkedin()
    new_page_title = shopping_page.get_title()
    assert "Jeremy" in new_page_title, f"Unexpected page title: {new_page_title}"
   
   
    
    # Optional: inspect captured network requests
    if network_logger:
        shopping_page.logger.info(f"Captured {len(network_logger)} network requests")    
    
    # Capture error message, if any
    error_text = shopping_page.get_error_message()

    # Log the captured text for debugging
    shopping_page.logger.info(f"Captured error message: {error_text!r}")

    # Assert that no error message is present
    assert not error_text, f"Unexpected error message found: {error_text}"