from playwright.sync_api import Page, Locator, expect

class WorkInNetherlandsSection:
    def __init__(self, page: Page):
        self.page = page

        # --- Section root ---
        self.section_root: Locator = page.locator(
            "div.sc-joc36b-0.ciyhZL:has(h4:has-text('Work in the Netherlands'))"
        )

        # --- Inner elements ---
        self.image: Locator = self.section_root.locator("div.sc-joc36b-1 img")
        self.heading: Locator = self.section_root.locator("h4:has-text('Work in the Netherlands')")
        self.paragraph: Locator = self.section_root.locator("div.sc-joc36b-3 p")
        self.linkedin_link: Locator = self.section_root.locator("div.sc-joc36b-3 p a")

    # --- helper methods ---
    #check expected elements are visible 
    def verify_section_visible(self):
        """Verify the section root and all key elements are visible."""
        expect(self.section_root).to_be_visible()
        expect(self.image).to_be_visible()
        expect(self.heading).to_be_visible()
        expect(self.paragraph).to_be_visible()
        expect(self.linkedin_link).to_be_visible()

    def get_heading_text(self) -> str:
        return self.heading.inner_text()

    def click_linkedin(self):
        expect(self.linkedin_link).to_be_visible()
        self.linkedin_link.click()
