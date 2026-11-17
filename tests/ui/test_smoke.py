
import pytest
from playwright.sync_api import expect
import re

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.contact_page import ContactPage

from pages.cart_page import CartPage
from pages.account_page import AccountPage

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


@pytest.mark.smoke
def test_smoke_login_invalid_credentials(page):
    """Mục tiêu: Kiểm tra đăng nhập với tài khoản không tồn tại.
    Điều kiện: Email không tồn tại và mật khẩu bất kỳ.
    Kết quả: Hiện lỗi Invalid email or password và vẫn ở trang login.
    """
    login = LoginPage(page).open()
    login.login("nobody-here@example.com", "WrongPassword123")

    expect(login.error).to_have_text("Invalid email or password")
    expect(page).to_have_url(re.compile(r".*/auth/login$"))

@pytest.mark.smoke
def test_smoke_contact_empty_form(page):
    """Mục tiêu: Kiểm tra xác thực Contact form khi để trống.
    Điều kiện: Mở trang Contact và không nhập dữ liệu.
    Kết quả: Hiện lỗi Subject is required và Message is required.
    """
    contact = ContactPage(page).open()
    contact.submit()

    expect(contact.subject_error).to_be_visible()
    expect(contact.message_error).to_be_visible()
    
 
# 8 test mới
@pytest.mark.smoke
def test_smoke_search_no_results(page):
    """Goal: Check search when no product matches.
    Condition: Search for a keyword that does not exist.
    Expected: The no-results message is displayed.
    """
    home = HomePage(page).open()
    home.search("zz-no-such-product-987xyz")

    expect(home.search_completed).to_be_visible()
    expect(home.no_results).to_be_visible()


@pytest.mark.smoke
def test_smoke_sort_products_by_price(page):
    """Goal: Check sorting products by price ascending.
    Condition: Open the product list and select price ascending.
    Expected: Product prices are ordered from low to high.
    """
    home = HomePage(page).open()
    home.sort_by("price,asc")

    expect(home.sorting_completed).to_be_visible()
    prices = home.prices()

    assert len(prices) > 1
    assert prices == sorted(prices)


@pytest.mark.smoke
def test_smoke_filter_hammer_category(page):
    """Goal: Check filtering products by Hammer category.
    Condition: Select the Hammer category.
    Expected: Every displayed product name contains Hammer.
    """
    home = HomePage(page).open()
    home.filter_by_category("Hammer")

    expect(home.product_names.first).to_be_visible()
    product_names = home.product_names.all_inner_texts()

    assert len(product_names) > 0
    for name in product_names:
        assert "hammer" in name.lower()


@pytest.mark.smoke
def test_smoke_product_detail_name_and_price(page):
    """Goal: Check product details.
    Condition: Open the Claw Hammer product.
    Expected: Its name and price are displayed correctly.
    """
    home = HomePage(page).open()
    product = home.open_product("Claw Hammer")

    expect(product.name).to_have_text("Claw Hammer")
    expect(product.unit_price).to_be_visible()
    assert product.price() > 0

@pytest.mark.smoke
def test_smoke_cart_line_total(page):
    """Goal: Check the line total in the cart.
    Condition: Add three Claw Hammers to the cart.
    Expected: Line total equals unit price multiplied by quantity.
    """
    home = HomePage(page).open()
    product = home.open_product("Claw Hammer")
    unit_price = product.price()

    product.add_to_cart(quantity=3)

    cart = product.go_to_cart()
    expect(cart.line_prices.first).to_be_visible()

    line_total = cart.line_totals()[0]
    assert round(line_total, 2) == round(unit_price * 3, 2)

@pytest.mark.smoke
def test_smoke_continue_shopping(page):
    """Goal: Check the Continue Shopping function.
    Condition: Add a product and open the cart.
    Expected: Continue Shopping returns to the product list.
    """
    home = HomePage(page).open()
    product = home.open_product("Claw Hammer")
    product.add_to_cart(quantity=1)

    cart = product.go_to_cart()
    cart.click_continue_shopping()

    expect(home.product_names.first).to_be_visible()

@pytest.mark.smoke
def test_smoke_login_empty_form(page):
    """Goal: Check required validation on the login form.
    Condition: Submit the login form without entering any data.
    Expected: Required validation messages are displayed.
    """
    login = LoginPage(page).open()
    login.submit_empty()

    expect(login.email_error).to_be_visible()
    expect(login.password_error).to_be_visible()


@pytest.mark.smoke
def test_smoke_logged_in_account(logged_in_page):
    """Goal: Check the account page after successful login.
    Condition: Open the account page using an authenticated session.
    Expected: Account title and account navigation are displayed.
    """
    account = AccountPage(logged_in_page).open()

    expect(account.title).to_be_visible()
    expect(account.nav_invoices).to_be_visible()
    expect(account.nav_profile).to_be_visible()

#B3.2