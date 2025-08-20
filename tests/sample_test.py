# tests/test_login.py
import pytest
from pages.shop_page import LoginPage

@pytest.mark.usefixtures("network_logger")  # Optional network logging
def test_invalid_login(page, network_logger):
    """
    Test invalid login to verify:
    - Error message appears
    - Logs are captured
    - Screenshot taken on failure
    - Network requests logged
    """
    login_page = LoginPage(page)
    
    # Navigate to login page
    login_page.goto("https://example.com/login")
    
    # Perform login with invalid credentials
    login_page.login("wronguser", "wrongpass")
    
    # Assert error message
    error_text = login_page.get_error_message()
    login_page.logger.info(f"Captured error message: {error_text}")
    assert error_text == "Invalid username or password"

    # Optional: inspect captured network requests
    if network_logger:
        login_page.logger.info(f"Captured {len(network_logger)} network requests")
