# Automation Exercise Playwright POM Simple

This project implements an end-to-end shopping cart flow on Automation Exercise:

https://automationexercise.com

##### Because i had issues with working on eBay site (They blocked me because of the automation tests i ran). ######

Automation Exercise is a demo e-commerce website built for automation practice, so it is a stable fit for this test exercise.

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


## Run

From this folder:

```powershell
python -m pytest tests\test_automation_exercise_cart_flow.py -q
```
