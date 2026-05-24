import pytest
from playwright.sync_api import sync_playwright

from automation_exercise_playwright_pom_simple.config.settings import settings

@pytest.fixture
def browser():
    with sync_playwright() as playwright:
        browser_type = getattr(playwright, settings.browser)
        print(
            f"\n[setup] launching {settings.browser}, channel={settings.browser_channel}, "
            f"headless={settings.headless}",
            flush=True,
        )
        launch_options = {
            "headless": settings.headless,
            "slow_mo": 500,
            "args": ["--disable-crash-reporter", "--start-maximized"],
        }
        if settings.browser_channel:
            launch_options["channel"] = settings.browser_channel
        browser = browser_type.launch(
            **launch_options,
        )
        print("[setup] browser launched", flush=True)
        yield browser
        browser.close()
        print("[teardown] browser closed", flush=True)

@pytest.fixture
def page(browser):
    print("[setup] creating browser context", flush=True)
    context = browser.new_context(no_viewport=True)
    context.set_default_timeout(settings.timeout_ms)
    context.set_default_navigation_timeout(settings.timeout_ms)
    page = context.new_page()
    print("[setup] page opened", flush=True)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield page
    context.tracing.stop(path="artifacts/traces/trace.zip")
    context.close()
    print("[teardown] context closed", flush=True)
