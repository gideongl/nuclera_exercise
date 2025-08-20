from playwright.sync_api import Page, Locator, TimeoutError as PlaywrightTimeoutError

def wait_for_element_visible(locator: Locator, timeout: float = 5000):
    locator.wait_for(state="visible", timeout=timeout)

def wait_for_element_hidden(locator: Locator, timeout: float = 5000):
    locator.wait_for(state="hidden", timeout=timeout)

def wait_for_text(locator: Locator, text: str, timeout: float = 5000):
    locator.wait_for(state="visible", timeout=timeout)
    locator.page.wait_for_function(
        "el => el.textContent.includes(text)",
        locator,
        timeout=timeout,
        arg=text
    )

def wait_for_url(page: Page, fragment: str, timeout: float = 5000):
    page.wait_for_url(f"**{fragment}**", timeout=timeout)
