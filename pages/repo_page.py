from playwright.sync_api import Page, Locator, expect, Download,sync_playwright, TimeoutError
import zipfile
from pathlib import Path
import logging
import os

logger = logging.getLogger("pytest_playwright")




class GitHubRepoPage:
    """
    Page Object Model for a GitHub repository page.
    Provides methods to check if the repo is public and downloadable.
    """
    def __init__(self, page: Page):
        self.page = page
        self.logger = logging.getLogger("pytest_playwright") # Use the same logger as in conftest.py


        # --- Locators ---
        #locator for code button
        #self.code_button: Locator = page.locator("button:has-text('Code')")
        self.code_button = self.page.get_by_role("button", name="Code")



        #locator for the code button menu
        self.code_menu = self.page.locator("div.react-overview-code-button-action-list")

        #sign in prompt locator to check if repo is private
        self.sign_in_prompt: Locator = self.page.locator("text=Sign in")
        #download zip link locator
        # Download ZIP link (the actual <a> inside the open dropdown)
        self.download_zip_link = self.page.locator("ul.prc-ActionList-ActionList-X4RiC >> a:has-text('Download ZIP')")




    #Return Page Title
    def get_title(self):
        return self.page.title()

    # Page-level methods
    def go_to(self, url: str):
        self.page.goto(url)


    # --- Methods ---
    def open_code_menu(self):
        """Open the Code dropdown menu if not already expanded."""
        if self.code_button.get_attribute("aria-expanded") != "true":
            self.code_button.click()
            expect(self.code_menu).to_be_visible()
            self.download_zip_link.wait_for(state="visible", timeout=5000)


    def is_public(self) -> bool:
        """
        Returns True if the repository is public (accessible without sign-in).
        """
        if self.sign_in_prompt.count() > 0:
            return False
        return self.code_button.is_visible()

    def can_access_download_zip(self) -> bool:
        """
        Returns True if the 'Download ZIP' link is visible and accessible.
        """
        if not self.is_public():
            return False

        try:
            # Wait for the Code button to be visible
            assert self.code_button.is_visible, "Code button not visible"
            self.open_code_menu()
            assert self.code_menu.is_visible(), "Code menu did not open"

            # Then wait for the Download ZIP link inside
            assert self.download_zip_link.is_visible
            return True
        except Exception:
            return False



    def download_zip(self, path: str):
        """
        Clicks the Download ZIP link in the Code menu and saves
        the downloaded file to the given path.
        """
        self.logger.info(f"Initiating download of ZIP file to {path}...")

        # Wait for the download to start when clicking the link
        with self.page.expect_download() as download_info:
            self.download_zip_link.click()

        download = download_info.value
        download.save_as(path)

        self.logger.info(f"Download completed: {path}")
        return download




    def verify_zip_contains_file(self, zip_path: str, filename: str = "README.md") -> bool:
        """Verify that the downloaded ZIP contains a specific file."""
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            filenames = zip_ref.namelist()
            self.logger.info(f"Files in ZIP '{zip_path}': {filenames}")

            if filename not in [f.split('/')[-1] for f in filenames]:
                self.logger.error(f"File '{filename}' not found in ZIP '{zip_path}'")
                assert False, f"{filename} not found in zip"

            self.logger.info(f"Verified '{filename}' exists in ZIP '{zip_path}'")
            return True