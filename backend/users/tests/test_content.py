import json
import math
import random
from unittest import skip

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

    def test_user_signup(self):
        user_count_ini = User.objects.count()
        tmp_signup_data = dict(constants.TEST_USER_DATA)
        ok_signup_data = tmp_signup_data
        rand_add = str((rnd := random.randint(1, 5)))

        for field in tmp_signup_data:
            tmp_signup_data[field] += rand_add
        # fmt: off
        tmp_signup_data["username"] += rand_add * rnd + "testing"[:rnd]
        tmp_signup_data["email"] = (
            f"test_user{rand_add * rnd}@example{rand_add}{'testing'[:rnd]}.org"
        )
        tmp_signup_data["password"] += rand_add
        # fmt: off
        response = self.client.post(
            constants.TEST_USERS_PAGE_URL,
            data=tmp_signup_data,
        )
        self.assertEqual(User.objects.count(), user_count_ini + 1)
        TestContent.DUMMY_DATA = tmp_signup_data
        del ok_signup_data["password"]
        # fmt: off
        self.assertIsNotNone(
            (uza := User.objects.get(
                username=tmp_signup_data["username"])
             )
        )
        ok_signup_data["id"] = uza.id
        self.assertEqual(json.loads(response.content), ok_signup_data)

    def test_user_gets_token_opens_me_page_deletes_token(self):
        u_count_ini = User.objects.count()
        self.test_user_signup()
        response = self.client.post(
            constants.TEST_USERS_PAGE_URL,
            data=TestContent.DUMMY_DATA,
        )
        self.assertEqual(User.objects.count(), u_count_ini + 1)
        # self.assertEqual(response.status_code, HTTPStatus.CREATED)
        #
        # token = self.get_token(
        #     {
        #         "password": constants.TEST_USER_DATA["password"],
        #         "email": constants.TEST_USER_DATA["email"],
        #     }
        # )
        # self.assertIn(constants.AUTH_TOKEN_FIELD, token)
        #
        # headers = {
        #     "Authorization": f"Token {token[constants.AUTH_TOKEN_FIELD]}",
        # }
        # response = self.client.get(
        #     constants.TEST_USER_ME_PAGE_URL,
        #     data={
        #         "password": constants.TEST_USER_DATA["password"],
        #         "email": constants.TEST_USER_DATA["email"],
        #     },
        #     headers=headers,
        # )
        # self.assertEqual(response.status_code, HTTPStatus.OK)
        #
        # response = self.client.post(
        #     constants.TEST_USER_TOKEN_OFF_URL,
        #     headers=headers,
        # )
        # self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
