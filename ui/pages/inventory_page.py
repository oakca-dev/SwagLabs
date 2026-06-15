from playwright.sync_api import Page

BASE_URL = "https://www.saucedemo.com"


class InventoryPage:
    URL = f"{BASE_URL}/inventory.html"

    def __init__(self, page: Page):
        self.page = page
        self.product_items = page.locator(".inventory_item")
        self.product_names = page.locator(".inventory_item_name")
        self.sort_dropdown = page.locator("[data-test='product-sort-container']")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_link = page.locator(".shopping_cart_link")
        self.burger_menu = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator("#logout_sidebar_link")
        self.all_items = page.locator("#inventory_sidebar_link")
        self.about = page.locator("#about_sidebar_link")
        self.reset_link = page.locator("#reset_sidebar_link")
        # Product detail page locators
        self.detail_name = page.locator(".inventory_details_name")
        self.detail_desc = page.locator(".inventory_details_desc")
        self.detail_price = page.locator(".inventory_details_price")
        self.detail_img = page.locator(".inventory_details_img")
        self.item_prices = page.locator(".inventory_item_price")

    def add_item_by_name(self, name: str):
        """Click the 'Add to cart' button for a product by its name."""
        btn_id = "add-to-cart-" + name.lower().replace(" ", "-").replace("(", "").replace(")", "")
        self.page.locator(f"[data-test='{btn_id}']").click()

    def remove_item_by_name(self, name: str):
        """Construct button id with the help of product name."""
        btn_id = "remove-" + name.lower().replace(" ", "-").replace("(", "").replace(")", "")
        self.page.locator(f"[data-test='{btn_id}']").click()

    def get_item_prices(self) -> list[float]:
        """Returns prices of all items on the screen as a list."""
        prices = self.item_prices.all_text_contents()
        return [float(p.replace("$", "")) for p in prices]

    def get_item_names(self) -> list[str]:
        """Returns names of all items on the screen as a list."""
        return self.product_names.all_text_contents()

    def click_first_product(self):
        """Click the first product name to open its detail page."""
        self.product_names.first.click()

    def sort_by(self, option_value: str):
        """option_value: 'az', 'za', 'lohi', 'hilo'"""
        self.sort_dropdown.select_option(option_value)

    def open_cart(self):
        self.cart_link.click()

    def logout(self):
        self.burger_menu.click()
        self.page.wait_for_selector("#logout_sidebar_link", state="visible")
        self.logout_link.click()
