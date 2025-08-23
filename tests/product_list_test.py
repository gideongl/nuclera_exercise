import pytest
from pages.shop_page import ShoppingPage

@pytest.mark.usefixtures("network_logger")
@pytest.mark.product_list
def test_dynamic_product_filters(page, network_logger):
    """
    Fully dynamic product list validation:
    - Iterates through all size filters dynamically
    - Verifies displayed product counts match UI-reported counts
    - Ensures each product has title, price, shipping info, and at least one image
    - Confirms total unfiltered product count remains consistent
    """
    shopping_page = ShoppingPage(page)

    # Navigate to shopping page
    shopping_page.goto("https://automated-test-evaluation.web.app/")
    shopping_page.verify_page_loaded()
    shopping_page.logger.info("Checking visibility of all elements on the product list page")

    # Verify product section visibility
    shopping_page.product_list_section.verify_section_visible()

    # Run dynamic size filter validation
    results = shopping_page.product_list_section.validate_all_sizes()

    # Log results for each size filter
    for size, count in results.items():
        shopping_page.logger.info(f"Size '{size}': {count} products displayed")
