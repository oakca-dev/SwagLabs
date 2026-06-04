"""
UI Tests – Authentication (TC-AUTH-*)

Covers:
  TC-AUTH-01  Successful login for all valid users
  TC-AUTH-02  Login blocked for locked_out_user
  TC-AUTH-03  Error shown for wrong password
  TC-AUTH-04  Error shown when username is blank
  TC-AUTH-05  Error shown when password is blank
  TC-AUTH-06  Logout navigates back to login page
  TC-AUTH-07  Protected routes redirect unauthenticated users to login
"""

import pytest
from playwright.sync_api import Page, expect
from ui.pages import LoginPage, InventoryPage
from ui.conftest import USERS, ERRORS, TEST_DATA, LOGIN_URL, INVENTORY_URL

# Users that can successfully log in (locked_out_user and perf_glitch excluded)
LOGINABLE_USERS = [
    (USERS["standard"]["username"], USERS["standard"]["password"]),
    (USERS["problem"]["username"],  USERS["problem"]["password"]),
    (USERS["error"]["username"],    USERS["error"]["password"]),
    (USERS["visual"]["username"],   USERS["visual"]["password"]),
]


class TestAuthentication:

    # ── TC-AUTH-01 ────────────────────────────────────────────────────────────
    @pytest.mark.parametrize("username, password", LOGINABLE_USERS)
    def test_user_can_login(self, page: Page, username: str, password: str):
        """Successful login lands on the inventory page for all valid users."""
        LoginPage(page).navigate().login(username, password)
        inv = InventoryPage(page)
        expect(page).to_have_url(INVENTORY_URL)
        expect(inv.product_items).not_to_have_count(0)

    # ── TC-AUTH-02 ────────────────────────────────────────────────────────────
    def test_locked_out_user_sees_error(self, page: Page):
        """locked_out_user is refused with a clear error message."""
        lp = LoginPage(page).navigate()
        lp.login(USERS["locked"]["username"], USERS["locked"]["password"])
        expect(lp.error_message).to_be_visible()
        expect(lp.error_message).to_have_text(ERRORS["locked_out"])

    # ── TC-AUTH-03 ────────────────────────────────────────────────────────────
    def test_wrong_password_shows_error(self, page: Page):
        """Incorrect password triggers credentials error."""
        lp = LoginPage(page).navigate()
        lp.login(USERS["standard"]["username"], TEST_DATA["wrong_password"])
        expect(lp.error_message).to_be_visible()
        expect(lp.error_message).to_have_text(ERRORS["wrong_password"])

    # ── TC-AUTH-04 ────────────────────────────────────────────────────────────
    def test_blank_username_shows_error(self, page: Page):
        """Submitting with no username shows a validation error."""
        lp = LoginPage(page).navigate()
        lp.login("", USERS["standard"]["password"])
        expect(lp.error_message).to_be_visible()
        expect(lp.error_message).to_have_text(ERRORS["username_required"])

    # ── TC-AUTH-05 ────────────────────────────────────────────────────────────
    def test_blank_password_shows_error(self, page: Page):
        """Submitting with no password shows a validation error."""
        lp = LoginPage(page).navigate()
        lp.login(USERS["standard"]["username"], "")
        expect(lp.error_message).to_be_visible()
        expect(lp.error_message).to_have_text(ERRORS["password_required"])

    # ── TC-AUTH-06 ────────────────────────────────────────────────────────────
    def test_logout_redirects_to_login(self, page: Page):
        """Clicking logout from the inventory page returns to login."""
        LoginPage(page).navigate().login(
            USERS["standard"]["username"], USERS["standard"]["password"]
        )
        InventoryPage(page).logout()
        expect(page).to_have_url(LOGIN_URL)
        expect(page.locator("#login-button")).to_be_visible()

    # ── TC-AUTH-07 ────────────────────────────────────────────────────────────
    def test_unauthenticated_user_lands_on_login(self, page: Page):
        """Navigating directly to a protected URL redirects to the login page."""
        page.goto(INVENTORY_URL)
        expect(page).to_have_url(LOGIN_URL)
        expect(page.locator("#login-button")).to_be_visible()
