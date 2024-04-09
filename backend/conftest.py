import pytest


@pytest.fixture(scope="module")
def get_standard_user_data():
    return {
        "url": "/api/users/",
        "token_url": "/api/auth/token/login/",
        "data": {
            "email": "standard@user.com",
            "username": "test_standard_uza",
            "first_name": "Test",
            "last_name": "Standard",
            "password": "wHat~Eva^_",
        },
    }
