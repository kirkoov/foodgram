import json

from django.contrib.auth import get_user_model
from django.test import TestCase

from backend import constants

User = get_user_model()


class TestContent(TestCase):
    # Increment by 1 for the paginator to create at least a 2nd users page
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

    def test_user_count(self):
        self.assertEqual(User.objects.count(), self.TOTAL)
        response = self.client.get(constants.TEST_USERS_PAGE)
        # fmt: off
        self.assertEqual(
            len(json.loads(response.content)["results"]), self.TOTAL - 1
        )

    def test_user_list_structure(self):
        response = self.client.get(constants.TEST_USERS_PAGE)
        self.assertEqual(
            json.loads(response.content).keys(),
            constants.TEST_USER_CONTENT_ITEMS.keys(),
        )
