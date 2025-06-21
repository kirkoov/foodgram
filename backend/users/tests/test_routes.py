import json
import math
import random
import sys
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase

from backend import constants


User = get_user_model()


class TestRoutes(TestCase):
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

    def test_user_pages_availability(self):
        limit = random.randint(1, TestRoutes.TOTAL)
        # fmt: off
        if User.objects.count() < constants.PAGINATOR_NUM:
            page = 1
        else:
            page = random.randint(
                1, (math.ceil(TestRoutes.TOTAL / constants.PAGINATOR_NUM))
            )
        urls_args_statuses = (
            (constants.TEST_USERS_PAGE_URL, None, HTTPStatus.OK),
            (constants.TEST_USERS_PAGE_URL, f"?limit={limit}", HTTPStatus.OK),
            (constants.TEST_USERS_PAGE_URL, f"?page={page}", HTTPStatus.OK),
            (constants.TEST_USERS_PAGE_URL, f"?limit=1&page={self.TOTAL}",
             HTTPStatus.OK),
            (constants.TEST_USERS_PAGE_URL, f"{limit}/", HTTPStatus.OK),
            (constants.TEST_USERS_PAGE_URL, f"{sys.maxsize}/",
             HTTPStatus.NOT_FOUND),
            (constants.TEST_USER_ME_PAGE_URL, None, HTTPStatus.UNAUTHORIZED),
        )
        for url, args, status in urls_args_statuses:
            # url = reverse(url, args=args)
            with self.subTest(url=url):
                if args is None:
                    response = self.client.get(url)
                else:
                    response = self.client.get(f"{url}{args}")
                self.assertEqual(response.status_code, status)

    def test_fail_signup_user(self):
        fail_data = dict(TestRoutes.DATA)
        fail_data["email"] = "invalid@email"
        fail_data2 = dict(constants.TEST_USER_DATA)
        fail_data2["username"] = ""
        urls_args_statuses = (
            (constants.TEST_USERS_PAGE_URL, fail_data, HTTPStatus.BAD_REQUEST),
            (
                constants.TEST_USERS_PAGE_URL,
                fail_data2,
                HTTPStatus.BAD_REQUEST,
            ),
        )
        for url, args, status in urls_args_statuses:
            with self.subTest(url=url):
                response = self.client.post(url, data=args)
                self.assertEqual(response.status_code, status)

    def test_user_signup(self):
        user_count_ini = User.objects.count()
        rand_add = str((rnd := random.randint(1, 5)))
        tmp_signup_data = dict(TestRoutes.DATA)
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
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(User.objects.count(), user_count_ini + 1)
        TestRoutes.DUMMY_DATA = tmp_signup_data

    def test_user_gets_token_opens_me_page_deletes_token(self):
        response = self.client.post(
            constants.TEST_USERS_PAGE_URL,
            data=constants.TEST_USER_DATA,
        )
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

        token = self.get_token(
            {
                "password": constants.TEST_USER_DATA["password"],
                "email": constants.TEST_USER_DATA["email"],
            }
        )
        self.assertIn(constants.AUTH_TOKEN_FIELD, token)

        headers = {
            "Authorization": f"Token {token[constants.AUTH_TOKEN_FIELD]}",
        }
        response = self.client.get(
            constants.TEST_USER_ME_PAGE_URL,
            data={
                "password": constants.TEST_USER_DATA["password"],
                "email": constants.TEST_USER_DATA["email"],
            },
            headers=headers,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response = self.client.post(
            constants.TEST_USER_TOKEN_OFF_URL,
            headers=headers,
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

    def test_fail_change_password(self):
        fail_data = {
            "new_password": TestRoutes.DATA["password"],
            "current_password": TestRoutes.DATA["password"],
        }

        response = self.client.post(
            constants.TEST_USER_PWD_CHANGE,
            data=fail_data,
        )
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

        self.test_user_signup()
        data_400 = {
            "new_password": "-",
            "current_password": TestRoutes.DUMMY_DATA["password"],
        }
        token = self.get_token(
            {
                "password": TestRoutes.DUMMY_DATA["password"],
                "email": TestRoutes.DUMMY_DATA["email"],
            }
        )
        headers = {
            "Authorization": f"Token {token[constants.AUTH_TOKEN_FIELD]}",
        }
        response = self.client.post(
            constants.TEST_USER_PWD_CHANGE,
            data=data_400,
            headers=headers,
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_change_password(self):
        self.test_user_signup()
        token = self.get_token(
            {
                "password": TestRoutes.DUMMY_DATA["password"],
                "email": TestRoutes.DUMMY_DATA["email"],
            }
        )
        headers = {
            "Authorization": f"Token {token[constants.AUTH_TOKEN_FIELD]}",
        }
        data_204 = {
            "new_password": TestRoutes.DUMMY_DATA["password"][1:],
            "current_password": TestRoutes.DUMMY_DATA["password"],
        }
        response = self.client.post(
            constants.TEST_USER_PWD_CHANGE,
            data=data_204,
            headers=headers,
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

    def get_token(self, user_data) -> str:
        response = self.client.post(
            constants.TEST_USER_TOKEN_ON_URL,
            data=user_data,
        )
        return json.loads(response.content)
