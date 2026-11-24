
import pytest
from playwright.sync_api import expect

from pages.base_page import BasePage


def money(text: str) -> float:
    """'$28.30' -> 28.3"""
    return float(text.replace("$", "").replace(",", "").strip())


class CartPage(BasePage):
    path = "/checkout"

    def __init__(self, page):
        super().__init__(page)
        self.product_titles = page.get_by_test_id("product-title")
        self.quantities = page.get_by_test_id("product-quantity")
        self.line_prices = page.get_by_test_id("line-price")
        self.total = page.get_by_test_id("cart-total")
        self.continue_shopping = page.get_by_test_id("continue-shopping")

    def line_totals(self) -> list[float]:
        return [money(t) for t in self.line_prices.all_inner_texts()]

    def total_value(self) -> float:
        return money(self.total.inner_text())

    def expect_quantity(self, quantity: int):
        expect(self.quantities).to_have_value(str(quantity))
        return self

    def expect_line_total(self, unit_price: float, quantity: int):
        totals = self.line_totals()

        assert len(totals) == 1
        assert totals[0] == pytest.approx(
            unit_price * quantity,
            abs=0.01
        )
        return self

    def click_continue_shopping(self):
        self.continue_shopping.click()
        return self
