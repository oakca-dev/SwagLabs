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

    def _navigate_to_login(self, page: Page) -> LoginPage:
        """Navigate to login page and return the LoginPage object."""
        return LoginPage(page).navigate()

    def _login_and_expect_error(self, page: Page, username: str, password: str, expected_error: str):
        """Attempt login with given credentials and assert error message matches."""
        lp = self._navigate_to_login(page)
        lp.login(username, password)
        expect(lp.error_message).to_be_visible()
        expect(lp.error_message).to_have_text(expected_error)

    def _assert_on_login_page(self, page: Page):
        """Assert the browser is on the login page with login button visible."""
        expect(page).to_have_url(LOGIN_URL)
        expect(page.locator("#login-button")).to_be_visible()

    # ── TC-AUTH-01 ────────────────────────────────────────────────────────────
    @pytest.mark.parametrize("username, password", LOGINABLE_USERS)
    def test_user_can_login(self, page: Page, username: str, password: str):
        """Successful login lands on the inventory page for all valid users."""
        self._navigate_to_login(page).login(username, password)
        expect(page).to_have_url(INVENTORY_URL)
        expect(InventoryPage(page).product_items).not_to_have_count(0)

    # ── TC-AUTH-02 ────────────────────────────────────────────────────────────
    def test_locked_out_user_sees_error(self, page: Page):
        """locked_out_user is refused with a clear error message."""
        self._login_and_expect_error(
            page, USERS["locked"]["username"], USERS["locked"]["password"],
            ERRORS["locked_out"]
        )

    # ── TC-AUTH-03 ────────────────────────────────────────────────────────────
    def test_wrong_password_shows_error(self, page: Page):
        """Incorrect password triggers credentials error."""
        self._login_and_expect_error(
            page, USERS["standard"]["username"], TEST_DATA["wrong_password"],
            ERRORS["wrong_password"]
        )

    # ── TC-AUTH-04 ────────────────────────────────────────────────────────────
    def test_blank_username_shows_error(self, page: Page):
        """Submitting with no username shows a validation error."""
        self._login_and_expect_error(
            page, "", USERS["standard"]["password"],
            ERRORS["username_required"]
        )

    # ── TC-AUTH-05 ────────────────────────────────────────────────────────────
    def test_blank_password_shows_error(self, page: Page):
        """Submitting with no password shows a validation error."""
        self._login_and_expect_error(
            page, USERS["standard"]["username"], "",
            ERRORS["password_required"]
        )

    # ── TC-AUTH-06 ────────────────────────────────────────────────────────────
    def test_logout_redirects_to_login(self, page: Page):
        """Clicking logout from the inventory page returns to login."""
        self._navigate_to_login(page).login(
            USERS["standard"]["username"], USERS["standard"]["password"]
        )
        InventoryPage(page).logout()
        self._assert_on_login_page(page)

    # ── TC-AUTH-07 ────────────────────────────────────────────────────────────
    def test_unauthenticated_user_lands_on_login(self, page: Page):
        """Navigating directly to a protected URL redirects to the login page."""
        page.goto(INVENTORY_URL)
        self._assert_on_login_page(page)
