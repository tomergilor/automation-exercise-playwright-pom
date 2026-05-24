import pytest
from pathlib import Path

from automation_exercise_playwright_pom_simple.pages.login_page import LoginPage
from automation_exercise_playwright_pom_simple.pages.search_page import SearchPage
from automation_exercise_playwright_pom_simple.pages.item_page import ItemPage
from automation_exercise_playwright_pom_simple.pages.cart_page import CartPage
from automation_exercise_playwright_pom_simple.utils.data_loader import DataLoader

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEST_CASES = DataLoader.load_json(PROJECT_ROOT / "data" / "search_cases.json")

@pytest.mark.e2e
@pytest.mark.parametrize("case", TEST_CASES, ids=[case["case_name"] for case in TEST_CASES])
def test_search_add_to_cart_and_validate_total(page, case):
    print(f"[test] starting case: {case['case_name']}", flush=True)
    login_page = LoginPage(page)
    search_page = SearchPage(page)
    item_page = ItemPage(page)
    cart_page = CartPage(page)

    print("[test] logging in", flush=True)
    login_page.login()

    print("[test] clearing cart", flush=True)
    cart_page.clear_cart()

    print(f"[test] searching for {case['query']} under {case['max_price']}", flush=True)
    urls = search_page.search_items_by_name_under_price(
        query=case["query"],
        max_price=case["max_price"],
        limit=case["limit"],
    )
    print(f"[test] found {len(urls)} item urls", flush=True)

    assert len(urls) > 0, "No items were found under the requested price"

    print("[test] adding items to cart", flush=True)
    item_page.add_items_to_cart(urls)
    print("[test] validating cart total", flush=True)
    cart_page.assert_cart_total_not_exceeds(
        budget_per_item=case["max_price"],
        items_count=len(urls),
    )
