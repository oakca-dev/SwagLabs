"""
UI Tests – Checkout Flow (TC-CHK-*)

Covers:
  TC-CHK-01  Happy-path checkout completes with confirmation message
  TC-CHK-02  Checkout with empty cart still reaches step-one
  TC-CHK-03  Step 1 – missing first name shows validation error
  TC-CHK-04  Step 1 – missing last name shows validation error
  TC-CHK-05  Step 1 – missing postal code shows validation error
  TC-CHK-06  Step 2 – order summary shows correct item subtotal
  TC-CHK-07  Step 2 – cancel returns to inventory
  TC-CHK-08  Completing checkout empties the cart
"""

import pytest
from playwright.sync_api import Page, expect
from ui.pages import (
    LoginPage, InventoryPage, CartPage,
    CheckoutFillInfoPage, CheckoutSummaryPage, CheckoutCompletePage,
)
from ui.conftest import (
    USERS, PRODUCTS, CHECKOUT,
    INVENTORY_URL, CHECKOUT_INFO_URL, CHECKOUT_SUMMARY_URL, CHECKOUT_DONE_URL,
)

ITEM = PRODUCTS["backpack"]
ORDER = CHECKOUT["order_info"]


class TestCheckout:

    @pytest.fixture(autouse=True)
    def _setup(self, page: Page):
        """Login and initialise shared page objects before each test."""
        LoginPage(page).navigate().login(
            USERS["standard"]["username"], USERS["standard"]["password"]
        )
        self.inv      = InventoryPage(page)
        self.cart     = CartPage(page)
        self.page     = page

    def _add_item_and_go_to_cart(self, item: str = ITEM):
        """Add one item and navigate to the cart page."""
        self.inv.add_item_by_name(item)
        self.inv.open_cart()

    def _proceed_to_fill_info(self, item: str = ITEM) -> CheckoutFillInfoPage:
        """Add item, open cart, click checkout, return fill-info page object."""
        self._add_item_and_go_to_cart(item)
        self.cart.checkout()
        return CheckoutFillInfoPage(self.page)

    # ── TC-CHK-01 ─────────────────────────────────────────────────────────────
    def test_checkout(self):
        """Full checkout flow completes and shows a confirmation."""
        fill_info = self._proceed_to_fill_info()
        fill_info.fill_info(ORDER["name"], ORDER["lastname"], ORDER["zipcode"])

        summary = CheckoutSummaryPage(self.page)
        expect(self.page).to_have_url(CHECKOUT_SUMMARY_URL)
        summary.finish()

        complete = CheckoutCompletePage(self.page)
        expect(self.page).to_have_url(CHECKOUT_DONE_URL)
        expect(complete.confirmation_header).to_have_text(CHECKOUT["thank_you_message_title"])
        expect(complete.order_complete_text).to_have_text(CHECKOUT["thank_you_message_info"])

        complete.back_home()
        expect(self.page).to_have_url(INVENTORY_URL)

    # ── TC-CHK-02 ─────────────────────────────────────────────────────────────
    def test_empty_cart_checkout(self):
        """Checkout from empty cart still navigates to step-one."""
        self.inv.open_cart()
        self.cart.checkout()
        expect(self.page).to_have_url(CHECKOUT_INFO_URL)

    # ── TC-CHK-03 ─────────────────────────────────────────────────────────────
    def test_missing_first_name_checkout(self):
        """Omitting first name shows a validation error."""
        fill_info = self._proceed_to_fill_info()
        fill_info.fill_info("", ORDER["lastname"], ORDER["zipcode"])
        expect(fill_info.error).to_have_text(CHECKOUT["first_name_required_error_message"])

    # ── TC-CHK-04 ─────────────────────────────────────────────────────────────
    def test_missing_last_name_checkout(self):
        """Omitting last name shows a validation error."""
        fill_info = self._proceed_to_fill_info()
        fill_info.fill_info(ORDER["name"], "", ORDER["zipcode"])
        expect(fill_info.error).to_have_text(CHECKOUT["last_name_required_error_message"])

    # ── TC-CHK-05 ─────────────────────────────────────────────────────────────
    def test_missing_postal_code_checkout(self):
        """Omitting postal code shows a validation error."""
        fill_info = self._proceed_to_fill_info()
        fill_info.fill_info(ORDER["name"], ORDER["lastname"], "")
        expect(fill_info.error).to_have_text(CHECKOUT["postal_code_required_error_message"])

    # ── TC-CHK-06 ─────────────────────────────────────────────────────────────
    def test_summary_page_shows_correct_subtotal(self):
        """Order summary subtotal matches the sum of cart item prices."""
        self._add_item_and_go_to_cart()
        expected_total = sum(self.cart.get_item_prices())

        self.cart.checkout()
        CheckoutFillInfoPage(self.page).fill_info(
            ORDER["name"], ORDER["lastname"], ORDER["zipcode"]
        )

        summary = CheckoutSummaryPage(self.page)
        subtotal_text = summary.price_without_tax.text_content()
        subtotal = float(subtotal_text.split("$")[1].strip())

        assert subtotal == pytest.approx(expected_total, abs=0.01), (
            f"Summary subtotal ${subtotal} doesn't match cart total ${expected_total}"
        )

    # ── TC-CHK-07 ─────────────────────────────────────────────────────────────
    def test_summary_page_cancel_returns_to_inventory(self):
        """Cancelling on the order summary page returns to inventory."""
        fill_info = self._proceed_to_fill_info()
        fill_info.fill_info(ORDER["name"], ORDER["lastname"], ORDER["zipcode"])
        CheckoutSummaryPage(self.page).cancel_btn.click()
        expect(self.page).to_have_url(INVENTORY_URL)

    # ── TC-CHK-08 ─────────────────────────────────────────────────────────────
    def test_cart_empty_after_order_complete(self):
        """After a successful order the cart badge is gone and cart is empty."""
        fill_info = self._proceed_to_fill_info()
        fill_info.fill_info(ORDER["name"], ORDER["lastname"], ORDER["zipcode"])
        CheckoutSummaryPage(self.page).finish()

        complete = CheckoutCompletePage(self.page)
        complete.back_home()
        expect(self.page).to_have_url(INVENTORY_URL)
        expect(self.inv.cart_badge).not_to_be_visible()

        self.inv.open_cart()
        expect(self.cart.cart_items).to_have_count(0)
