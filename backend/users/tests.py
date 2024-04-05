import json
import random

from django.contrib.auth import get_user_model
from django.db.utils import DataError
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APIRequestFactory, APITestCase

from api.views import UsersViewSet
from backend.constants import (
    NUM_CHARS_EMAIL,
    NUM_CHARS_FIRSTNAME,
    NUM_CHARS_LASTNAME,
    NUM_CHARS_USERNAME,
)
from .validators import is_email_valid  # , validate_username_field

User = get_user_model()


def get_admin_user_data():
    return {
        "email": "admin@user.com",
        "username": "test_admin_uza",
        "first_name": "John",
        "last_name": "Doe",
        "password": "Qwe``r~~ty12^3",
    }


def get_standard_user_data():
    return {
        "email": "standard@user.com",
        "username": "test_standard_uza",
        "first_name": "Test",
        "last_name": "Standard",
        "password": "wHat~Eva^_",
    }


class UserTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = APIRequestFactory()
        cls.prefix = "/api/"
        cls.users_rnd_create_limit = 11
        cls.users_url = f"{cls.prefix}users/"
        cls.test_users = []
        cls.request_users = cls.factory.get(cls.users_url)
        cls.view_user_detail = UsersViewSet.as_view({"get": "retrieve"})
        cls.client = APIClient()

        for index in range(random.randint(1, cls.users_rnd_create_limit)):
            user = User(
                username=f"test_uza{index}",
                first_name=f"First{index}",
                last_name=f"Last{index}",
                email=f"normal@user{index}.com",
                password=f"foo{index}Bar",
            )
            cls.test_users.append(user)
        User.objects.bulk_create(cls.test_users)
        cls.admin_user = User.objects.create_superuser(**get_admin_user_data())
        cls.test_users.append(cls.admin_user)
        # The user model has it that their ordering is by the emails
        cls.test_users = sorted(cls.test_users, key=lambda k: k.email)

    def test_create_superuser(self):
        self.assertEqual(self.admin_user.username, "test_admin_uza")
        self.assertEqual(self.admin_user.first_name, "John")
        self.assertEqual(self.admin_user.last_name, "Doe")
        self.assertEqual(self.admin_user.email, "admin@user.com")
        self.assertTrue(self.admin_user.is_active)
        self.assertTrue(self.admin_user.is_staff)
        self.assertTrue(self.admin_user.is_superuser)

    def test_list_users(self):
        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_users_limited(self):
        limit = len(self.test_users) - 1
        url_here = f"http://testserver/api/users/?limit={limit}"
        request_limited = self.factory.get(url_here)
        response = UsersViewSet.as_view({"get": "list"})(request_limited)
        data = response.__dict__.get("data")
        if data is not None:
            tmp_usernames = []
            self.assertEqual(data["count"], len(self.test_users))
            if limit == 0:
                self.assertIsNone(data["next"])
            else:
                self.assertEqual(data["next"], f"{url_here}&page=2")
            self.assertIsNone(data["previous"])
            for new, test in zip(data["results"], self.test_users):
                self.assertEqual(new["email"], test.email)
                self.assertTrue(len(new["email"]) <= NUM_CHARS_EMAIL)
                self.assertIsNone(is_email_valid(new["email"]))

                self.assertEqual(new["username"], test.username)
                self.assertTrue(len(new["username"]) <= NUM_CHARS_USERNAME)
                # assert validate_username_field(new["username"]) is None
                # A BUG must be here:
                # https://github.com/datamllab/tods/issues/58

                self.assertEqual(new["first_name"], test.first_name)
                self.assertTrue(len(new["first_name"]) <= NUM_CHARS_FIRSTNAME)

                self.assertEqual(new["last_name"], test.last_name)
                self.assertTrue(len(new["last_name"]) <= NUM_CHARS_LASTNAME)

                self.assertTrue(new["is_subscribed"] is False)  # By default it's False
                tmp_usernames.append(new["username"])
            # The usernames must be unique
            self.assertEqual(len(tmp_usernames), len(set(tmp_usernames)))
            self.assertEqual(len(data["results"]), limit)
        else:
            raise DataError("Users: no data in the test_list_users_limited().")

    def test_get_user_detail(self):
        id_ = 1
        request_detail = self.factory.get(f"{self.users_url}{id_}/")
        response = self.view_user_detail(request_detail, id=id_)
        if response.render():
            self.assertEqual(
                json.loads(response.content),
                {
                    "id": id_,
                    "email": f"normal@user{id_ - 1}.com",
                    "username": f"test_uza{id_ - 1}",
                    "first_name": f"First{id_ - 1}",
                    "last_name": f"Last{id_ - 1}",
                    "is_subscribed": False,
                },
            )
        else:
            raise DataError("No rendered content from the test_list_client_detail().")

    def test_get_userdetail_status404(self):
        # To make sure none as such exists, the multiplication is there
        request_detail = self.factory.get(
            f"{self.users_url}{self.users_rnd_create_limit * 2}/"
        )
        response = self.view_user_detail(
            request_detail, id=self.users_rnd_create_limit * 2
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_new_user_signup_201_pwdchange(self):
        response = self.client.post(
            self.users_url, get_standard_user_data(), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), len(self.test_users) + 1)
        data = response.__dict__.get("data")
        if data is not None:
            request_detail = self.factory.get(f"{self.users_url}{data['id']}/")
            response = self.view_user_detail(request_detail, id=data["id"])
            if response.render():
                test_data = get_standard_user_data()
                self.assertEqual(
                    json.loads(response.content),
                    {
                        "email": test_data["email"],
                        "id": data["id"],
                        "username": test_data["username"],
                        "first_name": test_data["first_name"],
                        "last_name": test_data["last_name"],
                        "is_subscribed": False,
                    },
                )

                user = User.objects.get(username=test_data["username"])
                client = APIClient()
                client.force_authenticate(user=user)
                pwd_data = {
                    "new_password": "akTFhB1aNmq9e2ZCnTfM",
                    "current_password": test_data["password"],
                }
                response = client.post(
                    f"{self.users_url}set_password/", pwd_data, format="json"
                )
                self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
                client.logout()
                client.login(
                    username=test_data["username"],
                    password=pwd_data["new_password"],
                )
                client.logout()

                client.force_authenticate(user=user)
                pwd_data = {
                    "new_password": pwd_data["new_password"],
                    # "current_password": test_data["password"],
                }
                response = client.post(
                    f"{self.users_url}set_password/", pwd_data, format="json"
                )
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                client.logout()
        else:
            raise DataError("Users: no data in the test_new_user_signup_201().")

    def test_new_user_signup_400(self):
        data = get_standard_user_data()
        data["password"] = "Qwerty123"  # Too common
        response = self.client.post(self.users_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), len(self.test_users))

    def test_user_pwd_change_401(self):
        data = get_standard_user_data()
        pwd_data = {
            "new_password": "akTFhB1aNmq9e2ZCnTfM",
            "current_password": data["password"],
        }
        response = self.client.post(
            f"{self.users_url}set_password/", pwd_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_user_gets_deletes_tokens(self):
        data = get_admin_user_data()
        test_data = {
            "password": data["password"],
            "email": data["email"],
        }
        response = self.client.post(
            f"{self.prefix}auth/token/login/", test_data, format="json"
        )
        self.assertTrue("auth_token" in response.__dict__["data"])
        self.assertTrue(isinstance(response.__dict__["data"]["auth_token"], str))

        response = self.client.post(f"{self.prefix}auth/token/logout/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        token = Token.objects.get(user__username=data["username"])
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.post(f"{self.prefix}auth/token/logout/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.client.logout()

    def test_new_standard_user_hits_me_url_200_401(self):
        data = get_standard_user_data()
        data["email"] = "standard@user.org"
        data["username"] = "standardUser"
        client = APIClient()
        response = client.post(self.users_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        test_data = {
            "password": data["password"],
            "email": data["email"],
        }
        response = client.post(
            f"{self.prefix}auth/token/login/", test_data, format="json"
        )
        self.assertTrue("auth_token" in response.__dict__["data"])

        token = Token.objects.get(user__username=data["username"])
        client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        response = self.client.get(f"{self.users_url}me/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = client.get(f"{self.users_url}me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        client.logout()
