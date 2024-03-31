import json
import random

from api.views import UsersViewSet
from backend.constants import (
    NUM_CHARS_EMAIL,
    NUM_CHARS_FIRSTNAME,
    NUM_CHARS_LASTNAME,
    NUM_CHARS_USERNAME,
)
from django.contrib.auth import get_user_model
from django.db.utils import DataError
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from .validators import is_email_valid  # , validate_username_field

User = get_user_model()


class UserTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = APIRequestFactory()
        cls.prefix = "/api/"

        cls.users_url = f"{cls.prefix}users/"
        cls.test_users = []
        cls.request_users = cls.factory.get(cls.users_url)
        cls.view_user_detail = UsersViewSet.as_view({"get": "retrieve"})

        for index in range(random.randint(1, 11)):
            user = User(
                username=f"test_uza{index}",
                first_name="First{index}",
                last_name="Last{index}",
                email=f"normal@user{index}.com",
                password="foo{index}Bar",
            )
            cls.test_users.append(user)
        User.objects.bulk_create(cls.test_users)
        cls.admin_user = User.objects.create_superuser(
            username="test_admin_uza",
            first_name="John",
            last_name="Doe",
            email="admin@user.com",
            password="bar~Foo",
        )
        cls.test_users.append(cls.admin_user)
        # The user model has it that their orderting is by the emails
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
        response = UsersViewSet.as_view({"get": "list"})(self.request_users)
        if response.status_code != 200:
            raise DataError("Users: no 200 status code for users.")

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

                self.assertTrue(
                    new["is_subscribed"] is False
                )  # By default it's False
                tmp_usernames.append(new["username"])
            # The usernames must be unique
            self.assertEqual(len(tmp_usernames), len(set(tmp_usernames)))
            self.assertEqual(len(data["results"]), limit)
        else:
            raise DataError("Users: no data in the test_list_users_limited().")

    # def test_list_client_detail(self):
    #     id_ = 2
    # request_detail = self.factory.get(
    #     f"http://127.0.0.1:8000/api/users/{id_}/"
    # )
    # response = self.view_detail(request_detail, id=id_)
    #     if response.render():
    #         self.assertEqual(
    #             json.loads(response.content),
    #             {
    #                 "id": id_,
    #                 "email": self.test_users[id_ - 1].email,
    #                 "username": self.test_users[id_ - 1].username,
    #                 "first_name": self.test_users[id_ - 1].first_name,
    #                 "last_name": self.test_users[id_ - 1].last_name,
    #                 "is_subscribed": False,
    #             },
    #         )
    #     else:
    #         raise DataError(
    #             "No rendered content from the test_list_client_detail()."
    #         )

    # def test_get_userdetail_status200(self):
    #     id_ = 1
    #     request_detail = self.factory.get(
    #         f"http://127.0.0.1:8000/api/users/{id_}/"
    #     )
    #     response = self.view_detail(request_detail, id=id_)
    #     assert response.status_code == 200

    # def test_get_userdetail_status404(self):
    #     request_detail = self.factory.get(
    #         f"http://127.0.0.1:8000/api/users/{maxsize}/"
    #     )
    #     response = self.view_detail(request_detail, id=maxsize)
    #     assert response.status_code == 404
