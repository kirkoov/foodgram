from http import HTTPStatus
from random import randint

import pytest

from backend.constants import TEST_TAG_PAGE_URL


@pytest.mark.parametrize(
    "status",
    (HTTPStatus.OK, HTTPStatus.OK),
)
@pytest.mark.parametrize(
    "url",
    (TEST_TAG_PAGE_URL, TEST_TAG_PAGE_URL + "1/"),
)
@pytest.mark.django_db
def test_tag_pages_for_anon_user(client, url, status):
    response = client.get(url)
    assert response.status_code == status


@pytest.mark.django_db
def test_tags_url_for_authenticated(admin_client):
    response = admin_client.get(TEST_TAG_PAGE_URL)
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
