from django.contrib.auth import get_user_model
from django.test import TestCase

from backend import constants

User = get_user_model()


class TestContent(TestCase):
    TOTAL = constants.PAGINATOR_NUM + 1

    @classmethod
    def setUpTestData(cls):
        User.objects.bulk_create(
            User(
                username=f"{constants.TEST_USER_DATA_2['username']}{idx}",
                first_name=f"{constants.TEST_USER_DATA_2['first_name']}{idx}",
                last_name=f"{constants.TEST_USER_DATA_2['last_name']}{idx}",
                email=f"{constants.TEST_USER_DATA_2['email']}{idx}",
                password=f"{constants.TEST_USER_DATA_2['password']}{idx}",
            )
            for idx in range(cls.TOTAL)
        )

    def test_number_users(self):
        self.assertEqual(User.objects.count(), self.TOTAL)
