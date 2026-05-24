# Automation Exercise Playwright POM Simple

This is a simplified copy of `automation_exercise_playwright_pom`.

The goal is to keep the same homework flow, but make the code easier to read and explain.

## What The Test Does

The main test is in:

```text
tests/test_automation_exercise_cart_flow.py
```

Flow:

1. Log in.
2. Clear the cart.
3. Search products by name.
4. Keep only products whose price is less than or equal to the max price.
5. Add the selected products to the cart.
6. Assert that the cart total does not exceed `max_price * items_count`.

## Test Data

The test data is in:

```text
data/search_cases.json
```

Example:

```json
{
  "query": "top",
  "max_price": 1200,
  "limit": 5
}
```

`pytest.mark.parametrize` sends each JSON object into the test as `case`.

## Main Files

```text
pages/login_page.py
```

Logs in to the website.

```text
pages/search_page.py
```

Searches products, reads each product price, filters by price, and returns product URLs.

```text
pages/item_page.py
```

Opens every product URL and clicks Add to cart.

```text
pages/cart_page.py
```

Reads the cart rows, sums the item totals, and checks the cart budget.

## Why This Version Is Simpler

The original project splits the search, add-to-cart, and cart-total logic into smaller helper methods.

This version keeps more of the logic inside the main functions, so the flow is easier to follow from top to bottom:

```python
search_page.search_items_by_name_under_price(...)
item_page.add_items_to_cart(...)
cart_page.assert_cart_total_not_exceeds(...)
```

## Run

From this folder:

```powershell
python -m pytest tests\test_automation_exercise_cart_flow.py -q
```
