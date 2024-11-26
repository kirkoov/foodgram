from http import HTTPStatus
from random import randint

import pytest

from backend.constants import TEST_TAG_PAGE_URL


@pytest.mark.django_db
def test_tags_url_for_anonymous(client):
    response = client.get(TEST_TAG_PAGE_URL)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_tags_url_for_authenticated(admin_client):
    response = admin_client.get(TEST_TAG_PAGE_URL)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_tag_id_url_for_anonymous200(client, create_test_tags):
    response = client.get(TEST_TAG_PAGE_URL + f"{randint(1, len(create_test_tags))}/")
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_tag_id_url_for_authenticated200(admin_client, create_test_tags):
    response = admin_client.get(
        TEST_TAG_PAGE_URL + f"{randint(1, len(create_test_tags))}/"
    )
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_tag_id_url_for_anonymous404(client, create_test_tags):
    response = client.get(TEST_TAG_PAGE_URL + f"{len(create_test_tags) + 1}/")
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
def test_tag_id_url_for_authenticated404(admin_client, create_test_tags):
    response = admin_client.get(TEST_TAG_PAGE_URL + f"{len(create_test_tags) + 1}/")
    assert response.status_code == HTTPStatus.NOT_FOUND


#
# def test_tags_id_url_for_anonymous(client):
#     response = client.get(TEST_TAG_PAGE_URL + "/1/")
#     assert response.status_code == HTTPStatus.NOT_FOUND


# @pytest.mark.parametrize(
#     'name',  # Имя параметра функции.
#     # Значения, которые будут передаваться в name.
#     ('notes:home', 'users:login', 'users:logout', 'users:signup')
# )
# # Указываем имя изменяемого параметра в сигнатуре теста.
# def test_pages_availability_for_anonymous_user(client, name):
#     url = reverse(name)  # Получаем ссылку на нужный адрес.
#     response = client.get(url)  # Выполняем запрос.
#     assert response.status_code == HTTPStatus.OK
