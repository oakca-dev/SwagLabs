"""
UI Tests – Inventory / Product Listing (TC-INV-*)

Covers:
  TC-INV-01  All 6 products are displayed
  TC-INV-02  Sort A→Z orders product names correctly
  TC-INV-03  Sort Z→A orders product names correctly
  TC-INV-04  Sort Price Low→High orders prices correctly
  TC-INV-05  Sort Price High→Low orders prices correctly
  TC-INV-06  Product detail page opens from inventory list
  TC-INV-07  Product detail page displays name, description, price and image
"""

import re
import pytest
from playwright.sync_api import Page, expect
from ui.pages import LoginPage, InventoryPage
from ui.conftest import USERS, INVENTORY_URL, SORT_OPTIONS

EXPECTED_PRODUCT_COUNT = 6


class TestInventory:

    @pytest.fixture(autouse=True)
    def _login(self, page: Page):
        """Log in before each test and initialise shared page objects."""
        LoginPage(page).navigate().login(
            USERS["standard"]["username"], USERS["standard"]["password"]
        )
        page.wait_for_url(INVENTORY_URL)
        self.inv = InventoryPage(page)
        self.page = page

    # ── TC-INV-01 ─────────────────────────────────────────────────────────────
    def test_all_products_displayed(self):
        """Inventory page shows all 6 products."""
        expect(self.inv.product_items).to_have_count(EXPECTED_PRODUCT_COUNT)

    # ── TC-INV-02 ─────────────────────────────────────────────────────────────
    def test_sort_name_a_to_z(self):
        """Sort A→Z renders product names in ascending alphabetical order."""
        self.inv.sort_by(SORT_OPTIONS["name_asc"])
        names = self.inv.get_item_names()
        assert names == sorted(names), f"Names not sorted A→Z: {names}"

    # ── TC-INV-03 ─────────────────────────────────────────────────────────────
    def test_sort_name_z_to_a(self):
        """Sort Z→A renders product names in descending alphabetical order."""
        self.inv.sort_by(SORT_OPTIONS["name_desc"])
        names = self.inv.get_item_names()
        assert names == sorted(names, reverse=True), f"Names not sorted Z→A: {names}"

    # ── TC-INV-04 ─────────────────────────────────────────────────────────────
    def test_sort_price_low_to_high(self):
        """Sort Price Low→High renders items with prices in ascending order."""
        self.inv.sort_by(SORT_OPTIONS["price_asc"])
        prices = self.inv.get_item_prices()
        assert prices == sorted(prices), f"Prices not sorted low→high: {prices}"

    # ── TC-INV-05 ─────────────────────────────────────────────────────────────
    def test_sort_price_high_to_low(self):
        """Sort Price High→Low renders items with prices in descending order."""
        self.inv.sort_by(SORT_OPTIONS["price_desc"])
        prices = self.inv.get_item_prices()
        assert prices == sorted(prices, reverse=True), f"Prices not sorted high→low: {prices}"

    # ── TC-INV-06 ─────────────────────────────────────────────────────────────
    def test_product_detail_opens(self):
        """Clicking a product name opens its detail page."""
        first_name = self.inv.get_item_names()[0]
        self.inv.click_first_product()
        expect(self.inv.detail_name).to_have_text(first_name)

    # ── TC-INV-07 ─────────────────────────────────────────────────────────────
    def test_product_detail_has_required_elements(self):
        """Product detail page shows name, description, price and image."""
        self.inv.click_first_product()
        expect(self.inv.detail_name).to_be_visible()
        expect(self.inv.detail_desc).to_be_visible()
        expect(self.inv.detail_price).to_be_visible()
        expect(self.inv.detail_img).to_be_visible()
