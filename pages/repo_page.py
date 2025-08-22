from playwright.sync_api import Page, Locator, expect, Download

class GitHubRepoPage:
    """
    Page Object Model for a GitHub repository page.
    Provides methods to check if the repo is public and downloadable.
    """
    def __init__(self, page: Page, repo_url: str):
        self.page = page
        self.repo_url = repo_url

        # --- Navigate to the repo page ---
        self.page.goto(repo_url, timeout=10000)

        # --- Locators ---
        self.code_button: Locator = self.page.locator("button:has-text('Code')")
        self.sign_in_prompt: Locator = self.page.locator("text=Sign in")
        self.download_zip_link: Locator = self.page.locator("a[aria-label*='Download ZIP']")

    # --- Methods ---
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
            expect(self.code_button).to_be_visible()
            self.code_button.click()
            expect(self.download_zip_link).to_be_visible()
            return True
        except Exception:
            return False

    def download_zip(self, save_path: str = None) -> Download:
        """
        Initiates download of the repository ZIP file.
        Returns the Playwright Download object for verification.
        If save_path is provided, the file is saved to that path.
        """
        if not self.can_access_download_zip():
            raise RuntimeError("Cannot access 'Download ZIP' link; repository may be private.")

        with self.page.expect_download() as download_info:
            self.download_zip_link.click()
        download = download_info.value

        if save_path:
            download.save_as(save_path)

        return download

