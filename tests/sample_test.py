# tests/test_login.py
import pytest
from pages.shop_page import ShoppingPage

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
    
    # Navigate to login page
    shopping_page.goto("https://automated-test-evaluation.web.app/")
    
    # Make Sure All Elements Are Visible
    shopping_page.logger.info("Checking visibility of all elements on the page")
    
    
    # Assert error message
    error_text = shopping_page.get_error_message()
    shopping_page.logger.info(f"Captured error message: {error_text}")
    assert error_text == "Not all expected elements are visible on the page", \
        f"Expected error message not found: {error_text}"   

    # Optional: inspect captured network requests
    if network_logger:
        shopping_page.logger.info(f"Captured {len(network_logger)} network requests")
