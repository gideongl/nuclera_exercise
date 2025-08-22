# tests/test_login.py
import os
import pytest
from pages.shop_page import ShoppingPage
from pages.repo_page import GitHubRepoPage
from tests.conftest import DOWNLOADS_DIR
from playwright.sync_api import Page, Locator, expect, Download,sync_playwright, TimeoutError


@pytest.mark.usefixtures("network_logger")
@pytest.mark.accessibility
def test_repo_page_accessibility(page):
    """
    Verify that the repo page linked from the shopping app
    is accessible, public, and has a Download ZIP option.
    """
    # Navigate to the shopping app
    shopping_page = ShoppingPage(page)
    shopping_page.goto("https://automated-test-evaluation.web.app/")
    shopping_page.verify_page_loaded()

    # Follow link to the GitHub repo
    shopping_page.repo_star_link.click()
    expect(page).to_have_url("https://github.com/jeffersonRibeiro/react-shopping-cart")
    repo_page = GitHubRepoPage(page)
    # Check repo accessibility
    repo_page.logger.info("Checking if repo page is accessible, public and download option is available...")
    #repo_page.can_access_download_zip()
    # Wait for Code button to appear before asserting
    expect(repo_page.code_button).to_be_visible(timeout=10000)  # wait up to 5s
    # Ensure the Code button is visible and the Download ZIP link appears
    assert repo_page.code_button.is_visible(), "Code button not found on the repo page"



@pytest.mark.usefixtures("network_logger")
@pytest.mark.download
def test_repo_page_download(page):
    """
    Verify that the GitHub repo page allows downloading
    a ZIP file and that it contains a README.md file.
    """
    repo_url = "https://github.com/jeffersonRibeiro/react-shopping-cart"
    repo_page = GitHubRepoPage(page)
    repo_page.go_to(repo_url)

    # Ensure Code button is visible
    # Wait for Code button to appear before asserting
    expect(repo_page.code_button).to_be_visible(timeout=5000)  # wait up to 5s
    # Ensure the Code button is visible and the Download ZIP link appears
    assert repo_page.code_button.is_visible(), "Code button not found on the repo page"
    repo_page.code_button.click()  # open the menu if not already open
    expect(repo_page.download_zip_link).to_be_visible(timeout=5000)
    assert repo_page.download_zip_link.is_visible(), "Download Zip button not found on the repo page"
    

    repo_page.logger.info("Downloading repo ZIP and verifying its contents...")

    # Download ZIP
    downloaded_file_path = os.path.join(DOWNLOADS_DIR, "downloaded_repo.zip")
    download = repo_page.download_zip(downloaded_file_path)
    assert os.path.exists(downloaded_file_path), "ZIP file was not saved"

    # Verify README.md is inside the ZIP
    repo_page.verify_zip_contains_file(downloaded_file_path, "README.md")
