from playwright.sync_api import Page

BASE_URL = "https://www.saucedemo.com"


class CheckoutFillInfoPage:
    URL = f"{BASE_URL}/checkout-step-one.html"

    def __init__(self, page: Page):
        self.page = page
        self.first_name = page.locator("[data-test='firstName']")
        self.last_name = page.locator("[data-test='lastName']")
        self.postal_code = page.locator("[data-test='postalCode']")
        self.continue_btn = page.locator("[data-test='continue']")
        self.cancel_btn = page.locator("[data-test='cancel']")
        self.error = page.locator("[data-test='error']")

    def fill_info(self, first: str, last: str, postal: str):
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(postal)
        self.continue_btn.click()

    def cancel_order(self):
        self.cancel_btn.click()
