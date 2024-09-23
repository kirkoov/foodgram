import json

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from backend import constants

User = get_user_model()


class TestLogic(TestCase):
    TOTAL = constants.TEST_NUM_USERS
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
        self.assertIn("detail", json.loads(response.content))

    def test_anonymous_user_cant_get_delete_token(self):
        fake_data = dict(TestLogic.DATA)
        fake_data["password"] = "mY-favaRiteFak0r"
        response = self.client.post(
            constants.TEST_USER_TOKEN_ON_URL,
            data=fake_data,
        )
        # fmt: off
        self.assertIn(
            "non_field_errors",
            json.loads(response.content)
        )
        response = self.client.post(
            constants.TEST_USER_TOKEN_OFF_URL,
        )
        self.assertIn("detail", json.loads(response.content))
