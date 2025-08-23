# tests/product_list_test.py
import pytest
from pages.shop_page import ShoppingPage

@pytest.mark.usefixtures("network_logger")
@pytest.mark.product_list
def test_dynamic_product_filters(page, network_logger):
    """
    Fully dynamic product list validation:
    - Validates all size filters dynamically
    - Verifies product counts per filter match UI-reported counts
    - Ensures each product has title, price, shipping info, and images
    - Confirms total unfiltered product count remains consistent
    """

    shopping_page = ShoppingPage(page)
    
    # Navigate to shopping page
    shopping_page.goto("https://automated-test-evaluation.web.app/")
    shopping_page.verify_page_loaded()
    shopping_page.logger.info("Checking visibility of all elements on the product list page")

    # Verify section is visible
    shopping_page.product_list_section.verify_section_visible()

    # Run dynamic size filter validation
    shopping_page.product_list_section.validate_all_sizes()

    # Optional: log network requests
    if network_logger:
        shopping_page.logger.info(f"Captured {len(network_logger)} network requests during product filter test")
