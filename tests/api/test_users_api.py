import pytest

from conftest import new_email, register_user, strong_password 

@pytest.mark.api
def test_register_empty_body_returns_422_with_field_errors(api):
    """Goal: server-side validation. Precondition: none.
    Expected: 422 and error lists for 'email' and 'password'."""
    response = api.post("/users/register", data={})
    assert response.status == 422, response.text()
    errors = response.json()
    assert "email" in errors and "password" in errors, errors

@pytest.mark.api
def test_register_leaked_password_is_rejected(api):
    """Goal: password policy. Precondition: none.
    Expected: 422 because 'Welcome01!' appears in known data leaks."""
    response = register_user(api, new_email(), "Welcome01!")
    assert response.status == 422, response.text()
    assert "password" in response.json()


# ---------------------------------------------------------------- B2.5 token
@pytest.mark.api
@pytest.mark.smoke
def test_users_me_with_token_returns_own_profile(api, auth_headers, test_user):
    """Goal: bearer token grants access. Precondition: user registered by the fixture.
    Expected: 200 and the same email."""
    response = api.get("/users/me", headers=auth_headers)
    assert response.status == 200, response.text()
    assert response.json()["email"] == test_user["email"]

