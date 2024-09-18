import json
import random

from django.contrib.auth import get_user_model
from django.test import TestCase
from users.validators import validate_username_field

from backend import constants

User = get_user_model()


class TestContent(TestCase):
    TOTAL = constants.TEST_NUM_USERS
    DATA = constants.TEST_USER_DATA_2
    DUMMY_DATA = None

    @classmethod
    def setUpTestData(cls):
        User.objects.bulk_create(
            User(
                username=f"{cls.DATA['username']}{idx}",
                first_name=f"{cls.DATA['first_name']}{idx}",
                last_name=f"{cls.DATA['last_name']}{idx}",
                email=f"test_user{idx}@example.org",
                password=f"{idx}{cls.DATA['password']}",
            )
            for idx in range(1, cls.TOTAL + 1)  # so that user id = DB id
        )

    def test_list_users(self):
        self.assertEqual((u_count := User.objects.count()), self.TOTAL)
        response = self.client.get(constants.TEST_USERS_PAGE_URL)
        self.assertEqual(
            (users_d := json.loads(response.content)).keys(),
            constants.TEST_USER_CONTENT_ITEMS.keys(),
        )
        # fmt: off
        self.assertEqual(
            len((user_d := users_d)["results"]), constants.PAGINATOR_NUM
        )
        self.assertEqual(user_d["count"], u_count)
        self.assertIn("?page=2", users_d["next"])
        self.assertIsNone(users_d["previous"])

        for u_d in users_d["results"]:
            self.assertEqual(
                u_d.keys(), constants.TEST_USER_CONTENT_RESULTS_ITEMS.keys()
            )
            self.assertTrue(
                len(u_d["username"]) <= constants.NUM_CHARS_USERNAME
            )
            self.assertTrue(validate_username_field(u_d["username"]))
            self.assertTrue(
                len(u_d["first_name"]) <= constants.NUM_CHARS_FIRSTNAME
            )
            self.assertTrue(
                len(u_d["last_name"]) <= constants.NUM_CHARS_LASTNAME
            )
            self.assertTrue(len(u_d["email"]) <= constants.NUM_CHARS_EMAIL)

    def test_users_page_with_limit(self):
        limit = random.randint(1, TestContent.TOTAL)
        # fmt: off
        if (u_count := User.objects.count()) < constants.PAGINATOR_NUM:
            # page = 1
            limit = random.randint(1, constants.PAGINATOR_NUM - 1)
        else:
            pass
            # page = random.randint(
            #     1, (math.ceil(TestContent.TOTAL / constants.PAGINATOR_NUM))
            # )
        response = self.client.get(constants.TEST_USERS_PAGE_URL + (
            f"?limit={limit}"
        ))
        self.assertEqual(
            (users_d := json.loads(response.content)).keys(),
            constants.TEST_USER_CONTENT_ITEMS.keys(),
        )
        # fmt: off
        self.assertEqual(
            len((user_d := users_d)["results"]), limit
        )
        self.assertEqual(user_d["count"], u_count)
        self.assertIsNone(users_d["previous"])
        for u_d in users_d["results"]:
            self.assertEqual(
                u_d.keys(), constants.TEST_USER_CONTENT_RESULTS_ITEMS.keys()
            )
            self.assertTrue(
                len(u_d["username"]) <= constants.NUM_CHARS_USERNAME
            )
            self.assertTrue(validate_username_field(u_d["username"]))
            self.assertTrue(
                len(u_d["first_name"]) <= constants.NUM_CHARS_FIRSTNAME
            )
            self.assertTrue(
                len(u_d["last_name"]) <= constants.NUM_CHARS_LASTNAME
            )
            self.assertTrue(len(u_d["email"]) <= constants.NUM_CHARS_EMAIL)
