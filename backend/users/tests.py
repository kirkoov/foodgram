import json
from json.decoder import JSONDecodeError

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from users.validators import validate_username_field

from backend.constants import (  # TEST_NUM_USERS,
    NUM_CHARS_EMAIL,
    NUM_CHARS_FIRSTNAME,
    NUM_CHARS_LASTNAME,
    NUM_CHARS_USERNAME,
)

User = get_user_model()


@pytest.mark.django_db
def test_list_users(
    api_client,
    get_standard_user_data,
    test_server_url,
    test_users_num,
    test_paginator_num,
    test_users_list_limit,
):
    test_users = []
    for idx in range(1, test_users_num):
        assert len(get_standard_user_data["data"]["username"]) <= NUM_CHARS_USERNAME
        assert (
            validate_username_field(get_standard_user_data["data"]["username"]) is True
        )
        assert len(get_standard_user_data["data"]["first_name"]) <= NUM_CHARS_FIRSTNAME
        assert len(get_standard_user_data["data"]["last_name"]) <= NUM_CHARS_LASTNAME
        assert len(get_standard_user_data["data"]["email"]) <= NUM_CHARS_EMAIL
        user = User(
            username=f"{get_standard_user_data['data']['username']}{idx}",
            first_name=f"{get_standard_user_data['data']['first_name']}{idx}",
            last_name=f"{get_standard_user_data['data']['last_name']}{idx}",
            email=f"standard@user{idx}.com",
            password=f"{get_standard_user_data['data']['password']}{idx}",
        )
        test_users.append(user)
    User.objects.bulk_create(test_users)
    response = api_client.get(get_standard_user_data["url"])
    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.content) == {
        "count": User.objects.count(),
        "next": f"{test_server_url}" f"{get_standard_user_data['url']}?page=2",
        "previous": None,
        "results": [
            {
                "email": x.email,
                "first_name": x.first_name,
                "id": x.id,
                "is_subscribed": False,
                "last_name": x.last_name,
                "username": x.username,
            }
            for x in User.objects.all()[:test_paginator_num]
        ],
    }
    response = api_client.get(f"{get_standard_user_data['url']}?page=2")
    assert response.status_code == status.HTTP_200_OK
    response = api_client.get(
        f"{get_standard_user_data['url']}?limit={test_users_list_limit}"
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(json.loads(response.content)["results"]) == test_users_list_limit


# @pytest.mark.django_db
# def test_user_sign_up_201(api_client, get_standard_user_data):
#     user_count_ini = User.objects.count()
#     response = api_client.post(
#         get_standard_user_data["url"],
#         get_standard_user_data["data"],
#         format="json",
#     )
#     assert response.status_code == status.HTTP_201_CREATED
#     assert User.objects.count() == user_count_ini + 1
#     id_ = 1
#     if user_count_ini == 2:
#         id_ = 3
#     assert json.loads(response.content) == {
#         "first_name": get_standard_user_data["data"]["first_name"],
#         "last_name": get_standard_user_data["data"]["last_name"],
#         "username": get_standard_user_data["data"]["username"],
#         "email": get_standard_user_data["data"]["email"],
#         "id": id_,
#     }
#     data = get_standard_user_data["data"]
#     data["email"] = "admin@user.com"
#     data["username"] = "admin"
#     User.objects.create_superuser(**data)
#     assert User.objects.count() == id_ + 1


@pytest.mark.django_db
def test_user_sign_up_400(api_client, get_standard_user_data):
    user_count_ini = User.objects.count()
    data = get_standard_user_data["data"]
    data["first_name"] = None
    data["password"] = None
    response = api_client.post(
        get_standard_user_data["url"],
        get_standard_user_data["data"],
        format="json",
    )
    assert json.loads(response.content) == {
        "first_name": ["This field may not be null."],
        "password": ["This field may not be null."],
    }
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert User.objects.count() == user_count_ini


# @pytest.mark.django_db
# def test_get_user_detail(api_client, get_standard_user_data):
#     id_ = 1
#     if User.objects.count() == 2:
#         id_ = 3
#     User.objects.create(**get_standard_user_data["data"])
#     response = api_client.get(f"{get_standard_user_data['url']}{id_}/")
#     assert json.loads(response.content) == {
#         "email": get_standard_user_data["data"]["email"],
#         "id": id_,
#         "username": get_standard_user_data["data"]["username"],
#         "first_name": get_standard_user_data["data"]["first_name"],
#         "last_name": get_standard_user_data["data"]["last_name"],
#         "is_subscribed": False,
#     }
#     if TEST_NUM_USERS < 1000:
#         response = api_client.get(f"{get_standard_user_data['url']}1000/")
#         assert response.status_code == status.HTTP_404_NOT_FOUND


# @pytest.mark.django_db  # test comment
# def test_get_user_me_url(api_client, get_standard_user_data):
#     id_ = 1
#     if User.objects.count() == 2:
#         id_ = 3
#     response = api_client.post(
#         get_standard_user_data["url"],
#         get_standard_user_data["data"],
#         format="json",
#     )
#     assert response.status_code == status.HTTP_201_CREATED
#     response = api_client.get(f"{get_standard_user_data['url']}me/")
#     assert response.status_code == status.HTTP_401_UNAUTHORIZED
#     test_data = {
#         "password": get_standard_user_data["data"]["password"],
#         "email": get_standard_user_data["data"]["email"],
#     }
#     response = api_client.post(
#         f"{get_standard_user_data['token_url']}", test_data, format="json"
#     )
#     assert "auth_token" in json.loads(response.content)
#     token = Token.objects.get(user__username=get_standard_user_data["data"]["username"])
#     api_client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
#     response = api_client.get(f"{get_standard_user_data['url']}me/")
#     api_client.logout()
#     assert response.status_code == status.HTTP_200_OK
#     assert json.loads(response.content) == {
#         "email": get_standard_user_data["data"]["email"],
#         "id": id_,
#         "username": get_standard_user_data["data"]["username"],
#         "first_name": get_standard_user_data["data"]["first_name"],
#         "last_name": get_standard_user_data["data"]["last_name"],
#         "is_subscribed": False,
#     }

## More changes for the sake of rerunning the foodgram via the
# workflow+githubactions


@pytest.mark.django_db
def test_user_pwd_change(api_client, get_standard_user_data):
    response = api_client.post(
        get_standard_user_data["url"],
        get_standard_user_data["data"],
        format="json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    user = User.objects.get(username=get_standard_user_data["data"]["username"])
    api_client.force_authenticate(user=user)
    pwd_data = {
        "new_password": "what_eVa$",
        "current_password": get_standard_user_data["data"]["password"],
    }
    response = api_client.post(
        get_standard_user_data["set_pwd_url"], pwd_data, format="json"
    )
    api_client.logout()
    assert response.status_code == status.HTTP_204_NO_CONTENT
    api_client.force_authenticate(user=user)
    pwd_data = {
        "new_password": "what_eVa$",
    }
    response = api_client.post(
        get_standard_user_data["set_pwd_url"], pwd_data, format="json"
    )
    api_client.logout()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    pwd_data = {
        "new_password": "new_0ne",
        "current_password": "0Ld_on1",
    }
    response = api_client.post(
        get_standard_user_data["set_pwd_url"], pwd_data, format="json"
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_user_gets_deletes_token(api_client, get_standard_user_data):
    response = api_client.post(
        get_standard_user_data["url"],
        get_standard_user_data["data"],
        format="json",
    )
    assert response.status_code == status.HTTP_201_CREATED

    response = api_client.post(f"{get_standard_user_data['del_token_url']}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    test_data = {
        "password": get_standard_user_data["data"]["password"],
        "email": get_standard_user_data["data"]["email"],
    }
    response = api_client.post(
        f"{get_standard_user_data['token_url']}", test_data, format="json"
    )
    assert response.status_code == status.HTTP_200_OK  # Tho 201 in the Docs...
    assert "auth_token" in json.loads(response.content)
    token = Token.objects.get(user__username=get_standard_user_data["data"]["username"])
    assert token is not None

    api_client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    response = api_client.post(f"{get_standard_user_data['del_token_url']}")
    api_client.logout()
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # Nothing in the response
    with pytest.raises(JSONDecodeError):
        json.loads(response.content)
