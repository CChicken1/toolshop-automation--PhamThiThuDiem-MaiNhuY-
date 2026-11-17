import pytest
# ---------------------------------------------------------------- B2.6 your own fixture
# TODO B2.6: write a fixture `new_cart` (in this file) that POSTs /carts and returns the id.
@pytest.fixture
def new_cart(api):
    response = api.post("/carts")
    assert response.status == 201, response.text()
    return response.json()["id"]

@pytest.mark.api
@pytest.mark.smoke
def test_cart_add_product_quantity_two_is_stored(api, new_cart):
    """Goal: cart API stores the quantity.
    Precondition: a new cart (your fixture) and the first product of GET /products.
    Expected: GET /carts/{id} has exactly 1 item, quantity 2, same product_id."""
    product = api.get("/products", params={"page": 1}).json()["data"][0]
    added = api.post(f"/carts/{new_cart}", data={"product_id": product["id"], "quantity": 2})
    assert added.ok, added.text()
    items = api.get(f"/carts/{new_cart}").json()["cart_items"]
    assert len(items) == 1
    assert items[0]["quantity"] == 2
    assert str(items[0]["product_id"]) == str(product["id"])
