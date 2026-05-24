from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from automation_exercise_playwright_pom_simple.pages.base_page import BasePage
from automation_exercise_playwright_pom_simple.utils.screenshot_helper import ScreenshotHelper


class ItemPage(BasePage):
    ADD_TO_CART_BUTTON = ".product-information button.cart, button:has-text('Add to cart')"
    CART_MODAL = "#cartModal"
    CONTINUE_SHOPPING_BUTTON = "#cartModal button:has-text('Continue Shopping')"

    def __init__(self, page):
        super().__init__(page)
        self.screenshots = ScreenshotHelper()

    def add_items_to_cart(self, urls: list[str]) -> None:
        for index, url in enumerate(urls, start=1):
            self.goto(url)
            add_to_cart_button = self.page.locator(self.ADD_TO_CART_BUTTON).first
            add_to_cart_button.wait_for(state="visible")
            add_to_cart_button.click()

            self.screenshots.take(self.page, f"item_{index}_added_to_cart")

            modal = self.page.locator(self.CART_MODAL)
            try:
                modal.wait_for(state="visible", timeout=5000)
                continue_button = self.page.locator(self.CONTINUE_SHOPPING_BUTTON).first
                if continue_button.count() > 0:
                    continue_button.click()
                    modal.wait_for(state="hidden", timeout=5000)
            except PlaywrightTimeoutError:
                pass
