"""
UI Tests – Authentication (TC-AUTH-*)

Covers:
  TC-AUTH-01  Successful login for all valid users (parametrized x4)
  TC-AUTH-02  Login blocked for locked_out_user
  TC-AUTH-03  Error shown for wrong password
  TC-AUTH-04  Error shown when username is blank
  TC-AUTH-05  Error shown when password is blank
  TC-AUTH-06  Error shown when both fields are empty
  TC-AUTH-07  Error shown for very long username (200 chars)
  TC-AUTH-08  Error shown for special characters username
  TC-AUTH-09  Logout navigates back to login page
  TC-AUTH-10  Protected routes redirect unauthenticated users to login
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

# Login error scenarios: (username, password, expected_error, test_id)
LOGIN_ERROR_CASES = [
    pytest.param(USERS["locked"]["username"], USERS["locked"]["password"], ERRORS["locked_out"], id="locked_user"),
    pytest.param(USERS["standard"]["username"], TEST_DATA["wrong_password"], ERRORS["wrong_password"], id="wrong_password"),
    pytest.param("", USERS["standard"]["password"], ERRORS["username_required"], id="blank_username"),
    pytest.param(USERS["standard"]["username"], "", ERRORS["password_required"], id="blank_password"),
    pytest.param("", "", ERRORS["username_required"], id="both_empty"),
    pytest.param(TEST_DATA["long_username"], USERS["standard"]["password"], ERRORS["wrong_password"], id="long_username"),
    pytest.param(TEST_DATA["special_chars_username"], USERS["standard"]["password"], ERRORS["wrong_password"], id="special_chars_username"),
]


class TestAuthentication:

    @staticmethod
    def _navigate_to_login(page: Page) -> LoginPage:
        """Navigate to login page and return the LoginPage object."""
        return LoginPage(page).navigate()

    @staticmethod
    def _assert_on_login_page(page: Page):
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

    # ── TC-AUTH-02/03/04/05 (parametrized) ────────────────────────────────────
    @pytest.mark.parametrize("username, password, expected_error", LOGIN_ERROR_CASES)
    def test_login_error(self, page: Page, username: str, password: str, expected_error: str):
        """Invalid login shows the correct error message."""
        lp = self._navigate_to_login(page)
        lp.login(username, password)
        expect(lp.error_message).to_have_text(expected_error)

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
