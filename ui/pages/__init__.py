"""
Re-export all Page Object Models so test files can use:
    from ui.pages import LoginPage, InventoryPage, ...
"""
from ui.pages.login_page import LoginPage
from ui.pages.inventory_page import InventoryPage
from ui.pages.cart_page import CartPage
from ui.pages.checkout_fill_info_page import CheckoutFillInfoPage
from ui.pages.checkout_summary_page import CheckoutSummaryPage
from ui.pages.checkout_complete_page import CheckoutCompletePage

__all__ = [
    "LoginPage",
    "InventoryPage",
    "CartPage",
    "CheckoutFillInfoPage",
    "CheckoutSummaryPage",
    "CheckoutCompletePage",
]
