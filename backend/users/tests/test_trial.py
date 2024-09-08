from unittest import skip

from django.contrib.auth import get_user_model
from django.test import TestCase  # Client,
from users.validators import validate_username_field

from backend import constants

User = get_user_model()


class TestUser(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(**constants.TEST_USER_DATA)
        # cls.user_client = Client()
        # cls.user_client.force_login(cls.user)

    @skip("Skipping trials")
    def test_user_there(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)
        # fmt: off
        self.assertEqual(self.user.username,
                         constants.TEST_USER_DATA["username"])
        # fmt: off
        self.assertTrue(
            len(self.user.username) <= constants.NUM_CHARS_USERNAME)
        # fmt: off
        self.assertTrue(validate_username_field(self.user.username))
        # fmt: off
        self.assertTrue(
            len(self.user.first_name) <= constants.NUM_CHARS_FIRSTNAME)
        # fmt: off
        self.assertTrue(
            len(self.user.last_name) <= constants.NUM_CHARS_LASTNAME)
        # fmt: off
        self.assertTrue(
            len(self.user.email) <= constants.NUM_CHARS_EMAIL)

    @skip("Skipping trials")
    def test_username(self):
        self.assertEqual(self.user.username, constants.TEST_USER_DATA["username"])
