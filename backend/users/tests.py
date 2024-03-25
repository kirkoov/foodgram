import json
from sys import maxsize

from django.contrib.auth import get_user_model
from django.db.utils import DataError
from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory

from api.views import UsersViewSet

User = get_user_model()


class UserTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = APIRequestFactory()
        cls.client = APIClient()
        cls.view = UsersViewSet.as_view({"get": "list"})
        cls.view_detail = UsersViewSet.as_view({"get": "retrieve"})
        cls.test_users = []
        for index in range(3):
            user = User(
                username=f"test_uza{index}",
                first_name="First",
                last_name="Last",
                email=f"normal@user{index}.com",
                password="foo",
            )
            cls.test_users.append(user)
        User.objects.bulk_create(cls.test_users)
        cls.admin_user = User.objects.create_superuser(
            username="test_admin_uza",
            first_name="John",
            last_name="Doe",
            email="admin@user.com",
            password="bar",
        )
        cls.test_users.append(cls.admin_user)

    def test_create_user(self):
        self.assertEqual(self.test_users[0].username, "test_uza0")
        self.assertEqual(self.test_users[0].first_name, "First")
        self.assertEqual(self.test_users[0].last_name, "Last")
        self.assertEqual(self.test_users[0].email, "normal@user0.com")
        self.assertTrue(self.test_users[0].is_active)
        self.assertFalse(self.test_users[0].is_staff)
        self.assertFalse(self.test_users[0].is_superuser)

    def test_create_superuser(self):
        self.assertEqual(self.admin_user.username, "test_admin_uza")
        self.assertEqual(self.admin_user.first_name, "John")
        self.assertEqual(self.admin_user.last_name, "Doe")
        self.assertEqual(self.admin_user.email, "admin@user.com")
        self.assertTrue(self.admin_user.is_active)
        self.assertTrue(self.admin_user.is_staff)
        self.assertTrue(self.admin_user.is_superuser)

    def test_list_clients(self):
        request = self.factory.get("http://127.0.0.1:8000/api/users")
        response = self.view(request)
        data = response.__dict__.get("data")
        if data is not None:
            self.assertEqual(len(data), len(self.test_users))
        else:
            raise DataError("No data in the test_clients().")

    def test_list_clients_limited(self):
        limit = 1
        request = self.factory.get(
            f"http://127.0.0.1:8000/api/users/?limit={limit}"
        )
        response = self.view(request)
        data = response.__dict__.get("data")
        if data is not None:
            self.assertEqual(data["count"], len(self.test_users))
            self.assertEqual(len(data["results"]), limit)
        else:
            raise DataError("No data in the test_list_clients_limited().")

    def test_list_client_detail(self):
        id_ = 2
        request_detail = self.factory.get(
            f"http://127.0.0.1:8000/api/users/{id_}/"
        )
        response = self.view_detail(request_detail, id=id_)
        if response.render():
            self.assertEqual(
                json.loads(response.content),
                {
                    "id": id_,
                    "email": self.test_users[id_ - 1].email,
                    "username": self.test_users[id_ - 1].username,
                    "first_name": self.test_users[id_ - 1].first_name,
                    "last_name": self.test_users[id_ - 1].last_name,
                    "is_subscribed": False,
                },
            )
        else:
            raise DataError(
                "No rendered content from the test_list_client_detail()."
            )

    def test_get_userdetail_status200(self):
        id_ = 1
        request_detail = self.factory.get(
            f"http://127.0.0.1:8000/api/users/{id_}/"
        )
        response = self.view_detail(request_detail, id=id_)
        assert response.status_code == 200

    def test_get_userdetail_status404(self):
        request_detail = self.factory.get(
            f"http://127.0.0.1:8000/api/users/{maxsize}/"
        )
        response = self.view_detail(request_detail, id=maxsize)
        assert response.status_code == 404
