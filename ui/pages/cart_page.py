from playwright.sync_api import Page

BASE_URL = "https://www.saucedemo.com"


class CartPage:
    URL = f"{BASE_URL}/cart.html"

    def __init__(self, page: Page):
        self.page = page
        self.cart_items = page.locator(".cart_item")
        self.item_names = page.locator(".inventory_item_name")
        self.item_prices = page.locator(".inventory_item_price")
        self.checkout_button = page.locator("[data-test='checkout']")
        self.continue_btn = page.locator("[data-test='continue-shopping']")
        self.remove_buttons_by_text = page.get_by_role("button", name="Remove")

    def get_item_names(self) -> list[str]:
        return self.item_names.all_text_contents()

    def get_item_prices(self) -> list[float]:
        """Returns prices of all items in the cart as a list of floats."""
        prices = self.item_prices.all_text_contents()
        return [float(p.replace("$", "").strip()) for p in prices]

    def checkout(self):
        self.checkout_button.click()

    def continue_shopping(self):
        self.continue_btn.click()

    def remove_item_by_name(self, name: str):
        """Remove an item by constructing the button locator from the item name."""
        remove_btn = f"[data-test='remove-{name.lower().replace(' ', '-')}']"
        self.page.locator(remove_btn).click()
