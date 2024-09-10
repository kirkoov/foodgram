import json
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase

from backend import constants

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(**constants.TEST_USER_DATA)

    def test_users_pages_availability(self):
        urls = (
            (constants.TEST_USERS_PAGE, None, HTTPStatus.OK),
            (constants.TEST_USER_PAGE_PAGENUM, None, HTTPStatus.OK),
            (constants.TEST_USER_PAGE_LIMIT, None, HTTPStatus.OK),
            (constants.TEST_USERS_PAGE, self.user.id, HTTPStatus.OK),
            (constants.TEST_USERS_PAGE, User.objects.count() + 1, HTTPStatus.NOT_FOUND),
            (constants.TEST_USER_OWN_PAGE, None, HTTPStatus.UNAUTHORIZED),
        )
        for url, args, status in urls:
            # url = reverse(url, args=args)
            with self.subTest(url=url):
                if args is None:
                    response = self.client.get(url)
                else:
                    response = self.client.get(f"{url}{args}/")
                self.assertEqual(response.status_code, status)

    def test_fail_signup_user(self):
        # fmt: off
        fail_data = constants.TEST_USER_DATA
        fail_data["email"] = "invalid@email"
        response = self.client.post(
            constants.TEST_USERS_PAGE,
            data=fail_data,
            # follow_redirects=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_signup_user(self):
        user_count_ini = User.objects.count()
        # fmt: off
        response = self.client.post(
            constants.TEST_USERS_PAGE,
            data=constants.TEST_USER_DATA_2,
        )
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(User.objects.count(), user_count_ini + 1)

    def test_get_token_see_me_page_delete_token(self):
        self.test_signup_user()
        token = self.get_token(
            {
                "password": constants.TEST_USER_DATA_2["password"],
                "email": constants.TEST_USER_DATA_2["email"],
            }
        )
        headers = {
            "Authorization": f"Token {token}",
        }
        response = self.client.get(
            constants.TEST_USER_OWN_PAGE,
            data={
                "password": constants.TEST_USER_DATA_2["password"],
                "email": constants.TEST_USER_DATA_2["email"],
            },
            headers=headers,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response = self.client.post(
            constants.TEST_USER_TOKEN_OFF,
            headers=headers,
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

    def test_user_fails_delete_token(self):
        response = self.client.post(
            constants.TEST_USER_TOKEN_OFF,
        )
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_fail_change_password(self):
        data = {
            "new_password": constants.TEST_USER_DATA_2["password"],
            "current_password": constants.TEST_USER_DATA_2["password"][1:],
        }
        response = self.client.post(
            constants.TEST_USER_PWD_CHANGE,
            data=data,
        )
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

        self.test_signup_user()
        data_400 = {
            "new_password": "-",
            "current_password": constants.TEST_USER_DATA_2["password"],
        }
        token = self.get_token(
            {
                "password": constants.TEST_USER_DATA_2["password"],
                "email": constants.TEST_USER_DATA_2["email"],
            }
        )
        headers = {
            "Authorization": f"Token {token}",
        }
        response = self.client.post(
            constants.TEST_USER_PWD_CHANGE,
            data=data_400,
            headers=headers,
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_change_password(self):
        self.test_signup_user()
        token = self.get_token(
            {
                "password": constants.TEST_USER_DATA_2["password"],
                "email": constants.TEST_USER_DATA_2["email"],
            }
        )
        headers = {
            "Authorization": f"Token {token}",
        }
        data_204 = {
            "new_password": constants.TEST_USER_DATA_2["password"][1:],
            "current_password": constants.TEST_USER_DATA_2["password"],
        }
        response = self.client.post(
            constants.TEST_USER_PWD_CHANGE,
            data=data_204,
            headers=headers,
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        response = self.client.get(
            constants.TEST_USER_OWN_PAGE,
            data={
                "password": data_204["new_password"],
                "email": constants.TEST_USER_DATA_2["email"],
            },
            headers=headers,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def get_token(self, user_data) -> str:
        response = self.client.post(
            constants.TEST_USER_TOKEN_ON,
            data=user_data,
        )
        # fmt: off
        self.assertTrue(
            "auth_token" in (tmp_d := json.loads(response.content))
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        return tmp_d["auth_token"]

    @staticmethod
    def delete_test_users():
        User.objects.all().delete()

    @classmethod
    def tearDownClass(cls):
        cls.delete_test_users()
