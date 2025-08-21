from playwright.sync_api import Page, expect

class WorkAbroadSection:
    def __init__(self, page: Page):
        self.page = page
        self.heading = page.locator('h4:has-text("Work in the Netherlands")')
        self.paragraph = page.locator('div.sc-joc36b-3 p')
        self.linkedin_link = page.locator('a[href="https://www.linkedin.com/in/jeremy-akeze-9542b396/"]')


    def verify_heading_visible(self):
        self.heading.wait_for(state='visible', timeout=5000)
        expect(self.heading).to_be_visible()

    def verify_paragraph_contains_text(self, text: str):
        self.paragraph.wait_for(state='visible', timeout=5000)
        expect(self.paragraph).to_contain_text(text)

    def click_linkedin_link(self):
        self.linkedin_link.wait_for(state='visible', timeout=5000)
        self.linkedin_link.click()
