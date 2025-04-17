import json
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from backend import constants

User = get_user_model()

# Minor changes


class TestLogic(TestCase):
    DATA = constants.TEST_USER_DATA
    client = Client()

    @classmethod
    def setUpTestData(cls):
        cls.client.post(
            constants.TEST_USERS_PAGE_URL,
            data=cls.DATA,
        )

    def test_anonymous_user_cant_change_password(self):
        data = {
            "new_password": TestLogic.DATA["password"][1:],
            "current_password": TestLogic.DATA["password"],
        }
        response = self.client.post(
            constants.TEST_USER_PWD_CHANGE,
            data=data,
        )
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_anonymous_user_cant_get_delete_token(self):
        fake_data = dict(TestLogic.DATA)
        fake_data["password"] = "mY-favaRiteFak0r"
        response = self.client.post(
            constants.TEST_USER_TOKEN_ON_URL,
            data=fake_data,
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        response = self.client.post(
            constants.TEST_USER_TOKEN_OFF_URL,
        )
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_user_cant_use_anothers_data(self):
        token_d = self.get_token(TestLogic.DATA)
        user_count_ini = User.objects.count()
        anothers_data = dict(TestLogic.DATA)
        anothers_data["username"] = "trangerCoco23"
        anothers_data["password"] = "VeRY02strangelYd_ifFernt~"
        anothers_data["email"] = "elYd@ya.org"
        self.client.post(
            constants.TEST_USERS_PAGE_URL,
            data=anothers_data,
        )
        self.assertEqual(User.objects.count(), user_count_ini + 1)

        pwd_change_data = {
            "new_password": anothers_data["password"][1:],
            "current_password": anothers_data["password"],
        }
        response = self.client.post(
            constants.TEST_USER_PWD_CHANGE,
            data=pwd_change_data,
            headers={
                "Authorization": f"Token {token_d[constants.AUTH_TOKEN_FIELD]}",
            },
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def get_token(self, user_data) -> str:
        response = self.client.post(
            constants.TEST_USER_TOKEN_ON_URL,
            data=user_data,
        )
        return json.loads(response.content)
