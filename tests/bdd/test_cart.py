
import pytest
from pytest_bdd import scenarios, given, when, then, parsers


from pages.home_page import HomePage


pytestmark = [pytest.mark.bdd, pytest.mark.ui]

scenarios("cart.feature")


@pytest.fixture
def cart_context():
    return {}


@given("the customer is on the product listing page")
def customer_on_listing_page(page, cart_context):
    cart_context["home"] = HomePage(page).open()


@when(parsers.parse('the customer searches for "{keyword}"'))
def customer_searches_product(keyword, cart_context):
    home = cart_context["home"]
    home.search(keyword)
    home.wait_search_completed()


@when(parsers.parse('the customer opens the "{product_name}" product'))
def customer_opens_product(product_name, cart_context):
    product = cart_context["home"].open_product(product_name)
    cart_context["product"] = product
    cart_context["unit_price"] = product.price()


@when(parsers.parse("the customer adds {quantity:d} units to the cart"))
def customer_adds_product(quantity, cart_context):
    cart_context["quantity"] = quantity
    cart_context["product"].add_to_cart(quantity)

@then(parsers.parse(
    "the shopping cart contains {quantity:d} units of the product"
))
def shopping_cart_contains_quantity(quantity, cart_context):
    cart = cart_context["product"].go_to_cart()
    cart_context["cart"] = cart
    cart.expect_quantity(quantity)


@then(parsers.parse(
    "the line total equals the unit price multiplied by {quantity:d}"
))
def line_total_is_correct(quantity, cart_context):
    cart_context["cart"].expect_line_total(
        cart_context["unit_price"],
        quantity
    )
