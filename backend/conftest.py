import pytest
from rest_framework.test import APIClient

from backend.constants import (
    PAGINATOR_NUM,
    TEST_LIMIT_LIST_USERS,
    TEST_NUM_USERS,
    TEST_SERVER_URL,
)


@pytest.fixture(scope="function")
def get_standard_user_data() -> dict:
    return {
        "url": "/api/users/",
        "token_url": "/api/auth/token/login/",
        "del_token_url": "/api/auth/token/logout/",
        "set_pwd_url": "/api/users/set_password/",
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


@pytest.fixture(scope="session")
def test_server_url() -> str:
    return TEST_SERVER_URL


@pytest.fixture(scope="session")
def test_users_num() -> int:
    return TEST_NUM_USERS


@pytest.fixture(scope="session")
def test_users_list_limit() -> int:
    return TEST_LIMIT_LIST_USERS


@pytest.fixture(scope="session")
def test_paginator_num() -> int:
    return PAGINATOR_NUM
