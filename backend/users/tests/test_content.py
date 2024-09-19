import json
import math
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

    def test_users_page_with_limit_page_params(self):
        base_url = constants.TEST_USERS_PAGE_URL
        limit = random.randint(1, TestContent.TOTAL)
        # fmt: off
        if (u_count := User.objects.count()) < constants.PAGINATOR_NUM:
            page = 1
            limit = random.randint(1, constants.PAGINATOR_NUM - 1)
        else:
            page = random.randint(
                1, (math.ceil(TestContent.TOTAL / constants.PAGINATOR_NUM))
            )
        urls = (
            base_url + f"?limit={limit}",
            base_url + f"?page={page}",
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(
                    (users_d := json.loads(response.content)).keys(),
                    constants.TEST_USER_CONTENT_ITEMS.keys(),
                )
                if "limit" in url:
                    self.assertIsNone(users_d["previous"])
                    self.assertEqual(
                        len((user_d := users_d)["results"]), limit
                    )
                self.assertEqual(user_d["count"], u_count)

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

    def test_fail_signup_user(self):
        failers = {
            "email": 123,
            "username": "",
            "first_name": "",
            "last_name": "",
            "password": "123Qwerty",
        }
        expected_error_data = {
            "first_name": ["This field may not be blank."],
            "last_name": ["This field may not be blank."],
            "username": ["This field may not be blank."],
            "email": ["Enter a valid email address."],
        }
        for failer in failers:
            fail_data = dict(TestContent.DATA)
            fail_data[failer] = failers[failer]
            response = self.client.post(
                constants.TEST_USERS_PAGE_URL,
                data=fail_data,
            )
            self.assertIn(failer, json.loads(response.content))

        response = self.client.post(
            constants.TEST_USERS_PAGE_URL,
            data=failers,
        )
        self.assertEqual(json.loads(response.content), expected_error_data)

        # fail_data2 = dict(constants.TEST_USER_DATA)
        # fail_data2[failers[1]] = ""
        #
        # response = self.client.post(
        #     constants.TEST_USERS_PAGE_URL,
        #     data=fail_data2,
        # )
        # self.assertIn(failers[1], json.loads(response.content))

        # urls_args_statuses = (
        #     (constants.TEST_USERS_PAGE_URL, fail_data, HTTPStatus.BAD_REQUEST),
        #     (constants.TEST_USERS_PAGE_URL, fail_data2, HTTPStatus.BAD_REQUEST),
        # )
        # for url, args, status in urls_args_statuses:
        #     with self.subTest(url=url):
        #         response = self.client.post(url, data=args)
        #         self.assertEqual(response.status_code, status)
