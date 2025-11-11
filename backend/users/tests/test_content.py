import json
import math
import random
from http import HTTPStatus

from django.contrib.auth import get_user_model

from backend import constants
from users.validators import validate_username_field
from users.tests.test_base import UserAuthTestMixin

User = get_user_model()


class TestContent(UserAuthTestMixin):
    TOTAL = constants.TEST_NUM_USERS
    DATA = constants.TEST_USER_DATA_2
    # DUMMY_DATA = None

    @classmethod
    def setUpTestData(cls):
        """
        Creates multiple users for tests that need a pre-populated database
        (e.g. pagination tests). This method runs once for the class.
        Note: User.objects.bulk_create does not call save() or hash passwords.
        For authentication tests, users should be created via _create_user.
        """
        # Ensure cls.DATA is available, or use a default if it's not a constant
        # Assuming constants.TEST_USER_DATA_2 is appropriate for bulk creation
        # if different from DUMMY_AUTH_DATA
        if hasattr(constants, "TEST_USER_DATA_2"):
            base_data = constants.TEST_USER_DATA_2
        else:
            base_data = {
                "username": "bulkuser",
                "first_name": "Bulk",
                "last_name": "User",
                "password": "bulkpassword",  # This password won't be hashed by
                # bulk_create
            }
        users_to_create = []
        for idx in range(1, cls.TOTAL + 1):
            user = User(
                username=f"{base_data['username']}{idx}",
                first_name=f"{base_data['first_name']}{idx}",
                last_name=f"{base_data['last_name']}{idx}",
                email=f"test_bulk_user{idx}@example.org",
                # Passwords aren't hashed by bulk_create, so this is just a
                # string. If these users need to be logged in, they must be
                # created one-by-one with create_user.
                password=f"{idx}{base_data['password']}",
            )
            users_to_create.append(user)
        User.objects.bulk_create(users_to_create)

    def setUp(self):
        """
        Set up for each test method. We do not create a user by default here
        as many tests in this class rely on the bulk-created users or
        create specific users for signup/auth scenarios.
        Individual tests will call self._create_user() if they need an
        authenticated user.
        """
        pass

    def test_list_users(self):
        self.assertEqual((u_count := User.objects.count()), self.TOTAL)
        response = self.client.get(constants.TEST_USERS_PAGE_URL, format="json")
        self.assertEqual(
            (users_d := response.data).keys(),
            constants.TEST_USER_CONTENT_ITEMS.keys(),
        )
        self.assertEqual(
            len((user_d := users_d)["results"]), constants.PAGINATOR_NUM
        )
        self.assertEqual(user_d["count"], u_count)
        # More robust check for 'next' link
        if users_d["next"]:
            # Check that 'next' contains a valid page parameter or structure
            self.assertIn("page=", users_d["next"])
        else:
            self.assertIsNone(users_d["next"])
        self.assertIsNone(users_d["previous"]) # For first page, should be None

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
        limit = random.randint(1, self.TOTAL)  # Use self.TOTAL

        # Determine a valid page number for testing
        if (u_count := User.objects.count()) < constants.PAGINATOR_NUM:
            page = 1
        else:
            page = random.randint(
                1,
                (
                    math.ceil(self.TOTAL / constants.PAGINATOR_NUM)
                ),  # Use self.TOTAL
            )

        # Define a list of URLs to test with expected number of results
        urls_and_expected_counts = [
            (f"{base_url}?limit={limit}", limit),
            (
                f"{base_url}?page={page}",
                constants.PAGINATOR_NUM
                if page < (math.ceil(self.TOTAL / constants.PAGINATOR_NUM))
                else self.TOTAL % constants.PAGINATOR_NUM
                or constants.PAGINATOR_NUM,
            ),
            (f"{base_url}?limit=1&page={self.TOTAL}", 1),
        ]

        # Add test for individual user detail page (e.g., /api/users/id/)
        first_user_id = (
            User.objects.first().id if User.objects.exists() else None
        )
        if first_user_id:
            urls_and_expected_counts.append(
                (f"{base_url}{first_user_id}/", "detail_view")
            )  # 'detail_view' as a special flag

        for url, expected_len_or_type in urls_and_expected_counts:
            with self.subTest(url=url):
                response = self.client.get(
                    url, format="json"
                )  # Use format='json'
                self.assertEqual(response.status_code, HTTPStatus.OK)
                users_d = response.data

                if expected_len_or_type == "detail_view":
                    # This is a detail view, so response should be a single object
                    self.assertEqual(users_d["id"], first_user_id)
                    self.assertEqual(
                        users_d.keys(),
                        constants.TEST_USER_CONTENT_RESULTS_ITEMS.keys(),
                    )
                else:
                    # This is a list view
                    self.assertEqual(
                        users_d.keys(),
                        constants.TEST_USER_CONTENT_ITEMS.keys(),
                    )
                    self.assertEqual(
                        len(users_d["results"]), expected_len_or_type
                    )
                    self.assertEqual(users_d["count"], u_count)

                    for u_d in users_d["results"]:
                        self.assertEqual(
                            u_d.keys(),
                            constants.TEST_USER_CONTENT_RESULTS_ITEMS.keys(),
                        )
                        self.assertTrue(
                            len(u_d["username"])
                            <= constants.NUM_CHARS_USERNAME
                        )
                        self.assertTrue(
                            validate_username_field(u_d["username"])
                        )
                        self.assertTrue(
                            len(u_d["first_name"])
                            <= constants.NUM_CHARS_FIRSTNAME
                        )
                        self.assertTrue(
                            len(u_d["last_name"])
                            <= constants.NUM_CHARS_LASTNAME
                        )
                        self.assertTrue(
                            len(u_d["email"]) <= constants.NUM_CHARS_EMAIL
                        )

    def test_users_page_with_limit_page_params_old(self):
        base_url = constants.TEST_USERS_PAGE_URL
        limit = random.randint(1, TestContent.TOTAL)

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
                        u_d.keys(),
                        constants.TEST_USER_CONTENT_RESULTS_ITEMS.keys(),
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
                    self.assertTrue(
                        len(u_d["email"]) <= constants.NUM_CHARS_EMAIL
                    )

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

        tmp_signup_data["username"] += rand_add * rnd + "testing"[:rnd]
        tmp_signup_data["email"] = (
            f"test_user{rand_add * rnd}@example{rand_add}{'testing'[:rnd]}.org"
        )
        tmp_signup_data["password"] += rand_add

        response = self.client.post(
            constants.TEST_USERS_PAGE_URL,
            data=tmp_signup_data,
        )
        self.assertEqual(User.objects.count(), user_count_ini + 1)
        TestContent.DUMMY_DATA = dict(tmp_signup_data)
        del ok_signup_data["password"]

        self.assertIsNotNone(
            (uza := User.objects.get(username=tmp_signup_data["username"]))
        )
        ok_signup_data["id"] = uza.id
        self.assertEqual(json.loads(response.content), ok_signup_data)

    def test_user_fails_me_page_get_delete_token(self):
        self.test_user_signup()
        test_data = {
            "password": TestContent.DUMMY_DATA["password"],
            "email": TestContent.DUMMY_DATA["email"],
        }
        headers = {
            "Authorization": "Token ",
        }
        response = self.client.get(
            constants.TEST_USER_ME_PAGE_URL,
            data=test_data,
            headers=headers,
        )
        self.assertIn("detail", json.loads(response.content))

        test_d = {
            "password": TestContent.DUMMY_DATA["password"][2:],
            "email": TestContent.DUMMY_DATA["email"],
        }
        self.assertIn("non_field_errors", self.get_token(test_d))

        response = self.client.post(
            constants.TEST_USER_TOKEN_OFF_URL,
            data=test_d,
            headers=headers,
        )
        self.assertIn("detail", json.loads(response.content))

    def test_user_gets_token_opens_me_page_deletes_token(self):
        self.test_user_signup()
        test_d = {
            "password": TestContent.DUMMY_DATA["password"],
            "email": TestContent.DUMMY_DATA["email"],
        }
        uza = User.objects.get(username=TestContent.DUMMY_DATA["username"])
        token_d = self.get_token(test_d)
        self.assertIn(constants.AUTH_TOKEN_FIELD, token_d)
        headers = {
            "Authorization": f"Token {token_d[constants.AUTH_TOKEN_FIELD]}",
        }
        response = self.client.get(
            constants.TEST_USER_ME_PAGE_URL,
            data=test_d,
            headers=headers,
        )
        self.assertEqual(
            (resp_d := json.loads(response.content)).keys(),
            constants.TEST_USER_CONTENT_RESULTS_ITEMS.keys(),
        )
        comp_data = dict(TestContent.DUMMY_DATA)
        comp_data["id"] = uza.id
        comp_data["is_subscribed"] = False
        del comp_data["password"]
        self.assertEqual(resp_d, comp_data)

        response = self.client.post(
            constants.TEST_USER_TOKEN_OFF_URL,
            headers=headers,
        )
        self.assertEqual(response.content, b"")
        response = self.client.get(
            constants.TEST_USER_ME_PAGE_URL,
            data=test_d,
            headers=headers,
        )
        self.assertIn("detail", json.loads(response.content))

    def test_fail_change_password(self):
        self.test_user_signup()
        test_ds = (
            {
                "password": TestContent.DUMMY_DATA["password"][2:],
                "email": TestContent.DUMMY_DATA["email"],
            },
            None,
            {
                "password": TestContent.DATA["password"],
                "email": TestContent.DATA["email"],
            },
        )
        for test_d in test_ds:
            response = self.client.post(
                constants.TEST_USER_PWD_CHANGE,
                data=test_d,
            )
            self.assertIn("detail", json.loads(response.content))
        token_d = self.get_token(
            {
                "password": TestContent.DUMMY_DATA["password"],
                "email": TestContent.DUMMY_DATA["email"],
            }
        )
        headers = {
            "Authorization": f"Token {token_d[constants.AUTH_TOKEN_FIELD]}",
        }
        data_400 = {
            "new_password": "-",
            "current_password": TestContent.DUMMY_DATA["password"][1:],
        }
        response = self.client.post(
            constants.TEST_USER_PWD_CHANGE,
            data=data_400,
            headers=headers,
        )
        self.assertIn("current_password", json.loads(response.content))

    def test_change_password(self):
        self.test_user_signup()
        user_data = {
            "password": TestContent.DUMMY_DATA["password"],
            "email": TestContent.DUMMY_DATA["email"],
        }
        token_d = self.get_token(user_data)
        headers = {
            "Authorization": f"Token {token_d[constants.AUTH_TOKEN_FIELD]}",
        }
        data_204 = {
            "new_password": TestContent.DUMMY_DATA["password"][1:],
            "current_password": TestContent.DUMMY_DATA["password"],
        }
        response = self.client.post(
            constants.TEST_USER_PWD_CHANGE,
            data=data_204,
            headers=headers,
        )
        self.assertEqual(response.content, b"")
        token_d = self.get_token(
            {
                "password": data_204["new_password"],
                "email": TestContent.DUMMY_DATA["email"],
            }
        )
        self.assertIn(constants.AUTH_TOKEN_FIELD, token_d)

    def get_token(self, user_data) -> str:
        response = self.client.post(
            constants.TEST_USER_TOKEN_ON_URL,
            data=user_data,
        )
        return json.loads(response.content)
