"""
UI Tests – Shopping Cart (TC-CART-*)

Covers:
  TC-CART-01  Adding one item updates cart badge to 1
  TC-CART-02  Adding multiple items reflects correct badge count
  TC-CART-03  Removing an item from inventory resets badge
  TC-CART-04  Cart page lists the correct items after adding
  TC-CART-05  Removing an item from cart page removes it from the list
  TC-CART-06  Cart persists items after navigating back to inventory
  TC-CART-07  Empty cart shows no items and zero badge
"""

import pytest
from playwright.sync_api import Page, expect
from ui.pages import LoginPage, InventoryPage, CartPage
from ui.conftest import USERS, PRODUCTS, CART_DATA, INVENTORY_URL

ITEM_1 = PRODUCTS["backpack"]
ITEM_2 = PRODUCTS["bike_light"]
ITEM_3 = PRODUCTS["bolt_shirt"]

ONE_ITEM_BADGE   = CART_DATA["one_item"]
THREE_ITEM_BADGE = CART_DATA["three_item"]


class TestCart:

    @pytest.fixture(autouse=True)
    def _login(self, page: Page):
        """Auto-login before each cart test and initialise shared page objects."""
        LoginPage(page).navigate().login(
            USERS["standard"]["username"], USERS["standard"]["password"]
        )
        self.inv  = InventoryPage(page)
        self.cart = CartPage(page)
        self.page = page

    # ── TC-CART-01 ────────────────────────────────────────────────────────────
    def test_add_single_item_updates_badge(self):
        """Adding one product shows cart badge '1'."""
        self.inv.add_item_by_name(ITEM_1)
        expect(self.inv.cart_badge).to_have_text(ONE_ITEM_BADGE)

    # ── TC-CART-02 ────────────────────────────────────────────────────────────
    def test_add_multiple_items_updates_badge(self):
        """Adding three products shows badge '3'."""
        for item in [ITEM_1, ITEM_2, ITEM_3]:
            self.inv.add_item_by_name(item)
        expect(self.inv.cart_badge).to_have_text(THREE_ITEM_BADGE)

    # ── TC-CART-03 ────────────────────────────────────────────────────────────
    def test_remove_from_inventory_resets_badge(self):
        """Removing the only item hides the cart badge."""
        self.inv.add_item_by_name(ITEM_1)
        expect(self.inv.cart_badge).to_have_text(ONE_ITEM_BADGE)
        self.inv.remove_item_by_name(ITEM_1)
        expect(self.inv.cart_badge).not_to_be_visible()

    # ── TC-CART-04 ────────────────────────────────────────────────────────────
    def test_cart_page_shows_added_items(self):
        """Cart page lists exactly the items that were added."""
        for item in [ITEM_1, ITEM_2]:
            self.inv.add_item_by_name(item)
        self.inv.open_cart()
        names = self.cart.get_item_names()
        assert ITEM_1 in names
        assert ITEM_2 in names
        assert len(names) == 2

    # ── TC-CART-05 ────────────────────────────────────────────────────────────
    def test_remove_from_cart_page(self):
        """Removing an item on the cart page removes it from the list."""
        self.inv.add_item_by_name(ITEM_1)
        self.inv.add_item_by_name(ITEM_2)
        self.inv.open_cart()
        self.cart.remove_item_by_name(ITEM_1)
        names = self.cart.get_item_names()
        assert ITEM_1 not in names
        assert ITEM_2 in names

    # ── TC-CART-06 ────────────────────────────────────────────────────────────
    def test_cart_persists_after_navigation(self):
        """Items added to the cart survive navigating back to the inventory."""
        self.inv.add_item_by_name(ITEM_1)
        self.inv.open_cart()
        self.cart.continue_shopping()
        expect(self.page).to_have_url(INVENTORY_URL)
        expect(self.inv.cart_badge).to_have_text(ONE_ITEM_BADGE)

    # ── TC-CART-07 ────────────────────────────────────────────────────────────
    def test_empty_cart_has_no_badge_and_no_items(self):
        """Cart shows no items and no badge when nothing has been added."""
        self.inv.open_cart()
        expect(self.cart.cart_items).to_have_count(0)
        expect(self.inv.cart_badge).not_to_be_visible()
