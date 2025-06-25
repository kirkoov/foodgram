import pytest
from rest_framework.test import APIClient

from backend.constants import (
    PAGINATOR_NUM,
    TEST_LIMIT_LIST_USERS,
    TEST_NUM_TAGS,
    TEST_NUM_USERS,
    TEST_SERVER_URL,
)
from recipes.models import Tag


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


# @pytest.fixture(scope="module")
# def engine():
#     # scope='session' | 'package'  | 'class'.
#     """Фикстура возвращает экземпляр класса двигателя."""
#     # print("Engine factory called")
#     return Engine()


# @pytest.fixture
# def start_engine(engine):  # Вызываем фикстуру получения объекта двигателя.
#     """Фикстура запускает двигатель."""
#     # Изменяем значение свойства объекта:
#     engine.is_running = True


# @pytest.fixture(autouse=True)
# def start_engine(engine):  # Вызываем фикстуру получения объекта двигателя.
#     """Фикстура запускает двигатель."""
#     engine.is_running = True
#     # print(f"Before test, engine.is_running: {engine.is_running}")
#     yield  # В этот момент начинает выполняться тест.
#     engine.is_running = False  # Заглушим двигатель.
#     # Распечатаем строчку после выполнения теста и остановки двигателя.
#     # print(f"After test engine.is_running {engine.is_running}")


@pytest.fixture(autouse=True)
def create_test_tags():
    test_tags = []
    for index in range(1, TEST_NUM_TAGS + 1):
        tag = Tag(
            name=f"Tag{index}",
            color=f"#E26C{index}D",
            slug=f"-{index}_slug",
        )
        test_tags.append(tag)
    Tag.objects.bulk_create(test_tags)
    return Tag.objects.all()
