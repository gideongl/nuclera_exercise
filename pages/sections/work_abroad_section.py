from playwright.sync_api import Page, expect

class WorkAbroadSection:
    def __init__(self, page: Page):
        self.page = page
        self.section_root = page.locator("div:has(h4:has-text('Work in the Netherlands'))")
        self.heading = self.section_root.locator("h4")
        self.paragraph = self.section_root.locator("p")
        self.linkedin_link = self.section_root.locator("a[href*='linkedin.com']")


    def verify_heading_visible(self):
        self.heading.wait_for(state='visible', timeout=5000)
        expect(self.heading).to_be_visible()

    def verify_paragraph_contains_text(self, text: str):
        self.paragraph.wait_for(state='visible', timeout=5000)
        expect(self.paragraph).to_contain_text(text)

    def click_linkedin_link(self):
        self.linkedin_link.wait_for(state='visible', timeout=5000)
        self.linkedin_link.click()
