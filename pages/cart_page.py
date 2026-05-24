from decimal import Decimal

from automation_exercise_playwright_pom_simple.config.settings import settings
from automation_exercise_playwright_pom_simple.pages.base_page import BasePage
from automation_exercise_playwright_pom_simple.utils.price_parser import PriceParser
from automation_exercise_playwright_pom_simple.utils.screenshot_helper import ScreenshotHelper


class CartPage(BasePage):
    CART_URL = f"{settings.base_url}/view_cart"
    CART_ROWS = "#cart_info_table tbody tr[id^='product-']"
    ROW_TOTAL = ".cart_total_price"
    DELETE_BUTTONS = ".cart_quantity_delete"

    def __init__(self, page):
        super().__init__(page)
        self.screenshots = ScreenshotHelper()

    def assert_cart_total_not_exceeds(self, budget_per_item: float, items_count: int) -> None:
        self.goto(self.CART_URL)
        rows = self.page.locator(self.CART_ROWS)
        rows.first.wait_for(state="attached", timeout=15000)

        actual_items_count = rows.count()
        assert actual_items_count == items_count, (
            f"Cart item count {actual_items_count} does not match expected count {items_count}"
        )

        total = Decimal("0")
        for index in range(rows.count()):
            total_text = rows.nth(index).locator(self.ROW_TOTAL).inner_text()
            line_total = PriceParser.parse_price(total_text)
            if line_total is None:
                raise AssertionError(f"Could not parse cart line total: {total_text}")
            total += line_total

        threshold = Decimal(str(budget_per_item)) * Decimal(items_count)
        print(f"[cart] total={total}, allowed={threshold}", flush=True)

        self.screenshots.take(self.page, "cart_total_page")
        assert total <= threshold, f"Cart total {total} exceeds allowed threshold {threshold}"

    def clear_cart(self) -> None:
        self.goto(self.CART_URL)
        delete_buttons = self.page.locator(self.DELETE_BUTTONS)
        while delete_buttons.count() > 0:
            row = self.page.locator(self.CART_ROWS).first
            row_id = row.get_attribute("id")
            delete_buttons.first.click()
            if row_id:
                self.page.locator(f"tr#{row_id}").wait_for(state="detached", timeout=15000)
