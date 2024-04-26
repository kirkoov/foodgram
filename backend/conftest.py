import pytest
from rest_framework.test import APIClient


@pytest.fixture(scope="session")
def get_standard_user_data_() -> dict:
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


@pytest.fixture(scope="session")
def api_client() -> APIClient:
    return APIClient()
