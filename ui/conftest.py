"""
UI conftest.py – browser, page fixtures and shared test data for all UI tests.
"""

import json
import pytest
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

# ── Shared test data ──────────────────────────────────────────────────────────
with open("test_data/ui/ui_test_data.json") as f:
    _TD = json.load(f)

USERS     = _TD["users"]
PRODUCTS  = _TD["products"]
ERRORS    = _TD["errors"]
TEST_DATA = _TD["test_data"]
CART_DATA = _TD["cart_data"]
CHECKOUT  = _TD["check_out_page_data"]
SORT_OPTIONS = _TD["sort_options"]

# ── URL constants ─────────────────────────────────────────────────────────────
BASE_URL             = "https://www.saucedemo.com"
LOGIN_URL            = BASE_URL + "/"
INVENTORY_URL        = BASE_URL + "/inventory.html"
CART_URL             = BASE_URL + "/cart.html"
CHECKOUT_INFO_URL    = BASE_URL + "/checkout-step-one.html"
CHECKOUT_SUMMARY_URL = BASE_URL + "/checkout-step-two.html"
CHECKOUT_DONE_URL    = BASE_URL + "/checkout-complete.html"

# ── Supported browsers ────────────────────────────────────────────────────────
SUPPORTED_BROWSERS = ("chromium", "firefox", "webkit")


# ── Create one shared browser instance for the entire test session ────────────
@pytest.fixture(scope="session")
def browser_instance(request):
    headed = request.config.getoption("--headed", default=False)
    browser_name = request.config.getoption("--browser", default="chromium")
    if isinstance(browser_name, list):
        browser_name = browser_name[0] if browser_name else "chromium"
    if browser_name not in SUPPORTED_BROWSERS:
        raise ValueError(f"Unsupported browser: {browser_name}. Choose from {SUPPORTED_BROWSERS}")
    with sync_playwright() as p:
        browser_type = getattr(p, browser_name)
        browser = browser_type.launch(headless=not headed)
        yield browser
        browser.close()


# ── Fresh Playwright page per test to avoid shared cookies/session state ──────
@pytest.fixture
def page(browser_instance: Browser):
    context: BrowserContext = browser_instance.new_context()
    page: Page = context.new_page()
    yield page
    context.close()
