from decimal import Decimal
from urllib.parse import urljoin

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from automation_exercise_playwright_pom_simple.config.settings import settings
from automation_exercise_playwright_pom_simple.pages.base_page import BasePage
from automation_exercise_playwright_pom_simple.utils.price_parser import PriceParser


class SearchPage(BasePage):
    PRODUCTS_URL = f"{settings.base_url}/products"
    SEARCH_INPUT = "#search_product"
    SEARCH_BUTTON = "#submit_search"
    PRODUCT_CARD_XPATH = "//div[contains(@class,'features_items')]//div[contains(@class,'product-image-wrapper')]"
    PRODUCT_PRICE_XPATH = ".//div[contains(@class,'productinfo')]//h2"
    PRODUCT_DETAILS_LINK_XPATH = ".//a[starts-with(@href, '/product_details/')]"
    NEXT_BUTTON = "a[rel='next'], a:has-text('Next'), .pagination a:has-text('>')"

    def search_items_by_name_under_price(self, query: str, max_price: float, limit: int = 5) -> list[str]:
        urls: list[str] = []
        max_allowed_price = Decimal(str(max_price))

        self.goto(self.PRODUCTS_URL)
        self.fill(self.page.locator(self.SEARCH_INPUT), query)
        self.click(self.page.locator(self.SEARCH_BUTTON))
        self.page.wait_for_load_state("domcontentloaded")

        while len(urls) < limit:
            product_cards = self.page.locator(f"xpath={self.PRODUCT_CARD_XPATH}")
            try:
                product_cards.first.wait_for(state="attached", timeout=15000)
            except PlaywrightTimeoutError:
                break

            print(f"[search] found {product_cards.count()} product cards on page", flush=True)

            for index in range(product_cards.count()):
                if len(urls) >= limit:
                    break

                product = product_cards.nth(index)
                price_text = product.locator(f"xpath={self.PRODUCT_PRICE_XPATH}").first.inner_text()
                price = PriceParser.parse_price(price_text)

                if price is None:
                    continue

                print(f"[search] product {index + 1}: price={price}", flush=True)

                if price > max_allowed_price:
                    continue

                link = product.locator(f"xpath={self.PRODUCT_DETAILS_LINK_XPATH}").first
                href = link.get_attribute("href")
                if href:
                    product_url = urljoin(settings.base_url, href)
                    if product_url not in urls:
                        urls.append(product_url)

            if len(urls) >= limit:
                break

            next_button = self.page.locator(self.NEXT_BUTTON).first
            if next_button.count() == 0:
                break

            next_button.click()
            self.page.wait_for_load_state("domcontentloaded")

        return urls
