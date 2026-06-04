# SwagLabs Automation Project


========================================
UI Automation:
========================================

UI Test Suite - Swag Labs (https://www.saucedemo.com)

========================================
1- Tools / Frameworks
========================================

Tool                    Version   Purpose
----------------------  -------   ----------------------------------------
Python                  3.13      Language
Playwright for Python   1.60      Browser automation, locators, assertions
pytest                  9.0       Test runner, fixtures, parametrize


========================================
2- How to Run
========================================

Install dependencies (first time only):
    pip install pytest playwright pytest-playwright
    playwright install chromium

Run all UI tests:
    python -m pytest ui/tests/ -v

Run a specific test file:
    python -m pytest ui/tests/test_auth.py -v
    python -m pytest ui/tests/test_cart.py -v
    python -m pytest ui/tests/test_checkout.py -v
    python -m pytest ui/tests/test_inventory.py -v


NOTE: Run UI and API tests separately. See api-tests.txt for API instructions.

========================================
 *** More info on flows.txt file
========================================


========================================
API Test Suite - Petstore Pet Endpoints:
========================================


========================================
1- Tools / Frameworks
========================================

Tool                    Version   Purpose
----------------------  -------   ----------------------------------------
Python                  3.13      Language
Playwright for Python   1.60      APIRequestContext for API calls, browser automation for UI
pytest                  9.0       Test runner, fixtures, assertions

Playwright's APIRequestContext is used for all API HTTP calls.
UI and API tests must be run in separate pytest sessions to avoid
asyncio conflicts.


========================================
2- How to Run
========================================

Install dependencies (first time only):
    pip install pytest playwright pytest-playwright
    playwright install chromium

IMPORTANT: UI and API tests must be run separately.
Playwright's sync API cannot run inside the asyncio event loop started
by pytest-playwright when UI and API tests run in the same session.

Run API tests only:
    python -m pytest api/tests/ -v

Run UI tests only:
    python -m pytest ui/tests/ -v

========================================
 *** More info on api-tests.txt file
========================================


