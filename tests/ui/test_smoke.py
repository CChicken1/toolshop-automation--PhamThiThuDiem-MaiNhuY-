
import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage


@pytest.mark.smoke
def test_smoke_search_pliers(page):
    """Mục tiêu: Kiểm tra chức năng tìm kiếm sản phẩm.
    Điều kiện: Trang chủ đã mở và tìm kiếm từ khóa pliers.
    Kết quả: Tất cả tên sản phẩm hiển thị đều chứa pliers.
    """
    home = HomePage(page).open()
    home.search("pliers")

    expect(home.search_completed).to_be_visible()

    product_names = home.product_names.all_inner_texts()

    assert len(product_names) > 0
    for name in product_names:
        assert "pliers" in name.lower()


@pytest.mark.smoke
def test_smoke_add_claw_hammer_to_cart(page):
    """Mục tiêu: Kiểm tra chức năng thêm sản phẩm vào giỏ hàng.
    Điều kiện: Sản phẩm Claw Hammer có trên trang chủ.
    Kết quả: Badge giỏ hàng hiển thị số lượng 3.
    """
    home = HomePage(page).open()
    product = home.open_product("Claw Hammer")
    product.add_to_cart(quantity=3)

    expect(home.cart_quantity).to_have_text("3")
