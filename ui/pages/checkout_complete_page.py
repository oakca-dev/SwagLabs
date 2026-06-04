from playwright.sync_api import Page

BASE_URL = "https://www.saucedemo.com"


class CheckoutCompletePage:
    URL = f"{BASE_URL}/checkout-complete.html"

    def __init__(self, page: Page):
        self.page = page
        self.confirmation_header = page.locator(".complete-header")
        self.order_complete_text = page.locator(".complete-text")
        self.back_home_btn = page.locator("[data-test='back-to-products']")

    def back_home(self):
        self.back_home_btn.click()
