from playwright.sync_api import Page

BASE_URL = "https://www.saucedemo.com"


class CheckoutSummaryPage:
    URL = f"{BASE_URL}/checkout-step-two.html"

    def __init__(self, page: Page):
        self.page = page
        self.finish_btn = page.locator("[data-test='finish']")
        self.cancel_btn = page.locator("[data-test='cancel']")
        self.price_without_tax = page.locator(".summary_subtotal_label")
        self.tax_value = page.locator(".summary_tax_label")
        self.price_total = page.locator(".summary_total_label")

    def get_total_price(self) -> float:
        """Returns total (subtotal + tax) price as a float."""
        p_text = self.price_total.text_content()
        # e.g. "Total: $32.39" → 32.39
        return float(p_text.split("$")[1].strip())

    def finish(self):
        self.finish_btn.click()
