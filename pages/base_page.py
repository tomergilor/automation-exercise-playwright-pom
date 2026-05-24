from playwright.sync_api import Page, Locator, expect

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self, url: str) -> None:
        print(f"[nav] goto {url}", flush=True)
        self.page.goto(url, wait_until="commit", timeout=15000)
        print(f"[nav] loaded {self.page.url}", flush=True)

    def click(self, locator: Locator) -> None:
        locator.wait_for(state="visible")
        locator.click()

    def fill(self, locator: Locator, text: str) -> None:
        locator.wait_for(state="visible")
        locator.fill(text)

    def text(self, locator: Locator) -> str:
        locator.wait_for(state="visible")
        return locator.inner_text().strip()

    def assert_visible(self, locator: Locator) -> None:
        expect(locator).to_be_visible()
