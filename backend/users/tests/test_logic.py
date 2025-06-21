from http import HTTPStatus

from django.contrib.auth import get_user_model
from users.tests.test_base import UserAuthTestMixin  # Import the new mixin

from backend import constants


User = get_user_model()


class TestLogic(UserAuthTestMixin):  # Inherit from the new mixin
    @classmethod
    def setUpTestData(cls):
        """
        For TestLogic, we might still want a base user to exist for some tests
        or we create them in setUp.
        The initial setup of one user can be done here for efficiency if
        multiple tests in this class rely on the same initial user state.
        If tests require different user states, it's better to create users in setUp.
        """
        # Example: if a test needs a pre-existing user without needing to log them in,
        # create_user_model will just create the Django user object.
        # cls.initial_user = User.objects.create_user(
        #     username="initialuser", email="initial@example.org", password="password123"
        # )
        pass  # Leaving empty as per your original refactoring path, users will be created in setUp or test method.

    def setUp(self):
        """
        Set up for each test method. We'll create our primary test user here.
        This ensures each test method runs with a clean database and a
        freshly created user for authentication scenarios.
        """
        self.user, self.user_data = self._create_user(
            user_data=dict(self.DUMMY_AUTH_DATA)
        )
        # self.user_data now contains the data used to create self.user

    def test_anonymous_user_cant_change_password(self):
        # No change needed here, as it tests an unauthorised scenario.
        data = {
            "new_password": self.user_data["password"][
                1:
            ],  # Use self.user_data
            "current_password": self.user_data["password"],
        }
        response = self.client.post(
            constants.TEST_USER_PWD_CHANGE,
            data=data,
            format="json",  # Explicitly send as JSON
        )
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_anonymous_user_cant_get_delete_token(self):
        # No change needed here, as it tests unauthorised scenarios.
        # The fake_data is independent of the user created in setUp.
        fake_data = dict(self.user_data)  # Use self.user_data as a base
        fake_data["password"] = "mY-favaRiteFak0r"
        response = self.client.post(
            constants.TEST_USER_TOKEN_ON_URL, data=fake_data, format="json"
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        # Test deletion without token
        response = self.client.post(
            constants.TEST_USER_TOKEN_OFF_URL,
            # No data needed for logout generally
        )
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_user_cant_use_anothers_data(self):
        # Authenticate the primary user created in setUp
        # Using _get_auth_headers for conciseness
        headers_primary_user = self._get_auth_headers(
            self.user_data["email"], self.user_data["password"]
        )

        user_count_ini = User.objects.count()  # Should be 1 (from setUp)

        # Create a second, "another" user using the helper
        anothers_data = {
            "username": "trangerCoco23",
            "password": "VeRY02strangelYd_ifFernt~",
            "email": "elYd@ya.org",
            "first_name": "Another",
            "last_name": "User",
        }
        self._create_user(anothers_data)  # Create the second user
        self.assertEqual(
            User.objects.count(), user_count_ini + 1
        )  # Verify count increased

        # Try to change the second user's password using the primary user's token
        pwd_change_data = {
            "new_password": anothers_data["password"][1:],
            "current_password": anothers_data[
                "password"
            ],  # This should be the other user's current password
            "email": anothers_data[
                "email"
            ],  # Potentially needed if serializer uses email for lookup
        }
        response = self.client.post(
            constants.TEST_USER_PWD_CHANGE,
            data=pwd_change_data,
            headers=headers_primary_user,  # Use primary user's token
            format="json",
        )
        # Expect BAD_REQUEST because primary user is trying to change another's password
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        # Verify the password of the 'another' user hasn't changed (optional but good)
        another_user_obj = User.objects.get(email=anothers_data["email"])
        self.assertTrue(
            another_user_obj.check_password(anothers_data["password"])
        )


# # Old tests of mine
# class TestLogic(TestCase):
#     DATA = constants.TEST_USER_DATA
#     client = Client()
#
#     @classmethod
#     def setUpTestData(cls):
#         cls.client.post(
#             constants.TEST_USERS_PAGE_URL,
#             data=cls.DATA,
#         )
#
#     def test_anonymous_user_cant_change_password(self):
#         data = {
#             "new_password": TestLogic.DATA["password"][1:],
#             "current_password": TestLogic.DATA["password"],
#         }
#         response = self.client.post(
#             constants.TEST_USER_PWD_CHANGE,
#             data=data,
#         )
#         self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
#
#     def test_anonymous_user_cant_get_delete_token(self):
#         fake_data = dict(TestLogic.DATA)
#         fake_data["password"] = "mY-favaRiteFak0r"
#         response = self.client.post(
#             constants.TEST_USER_TOKEN_ON_URL,
#             data=fake_data,
#         )
#         self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
#         response = self.client.post(
#             constants.TEST_USER_TOKEN_OFF_URL,
#         )
#         self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
#
#     def test_user_cant_use_anothers_data(self):
#         token_d = self.get_token(TestLogic.DATA)
#         user_count_ini = User.objects.count()
#         anothers_data = dict(TestLogic.DATA)
#         anothers_data["username"] = "trangerCoco23"
#         anothers_data["password"] = "VeRY02strangelYd_ifFernt~"
#         anothers_data["email"] = "elYd@ya.org"
#         self.client.post(
#             constants.TEST_USERS_PAGE_URL,
#             data=anothers_data,
#         )
#         self.assertEqual(User.objects.count(), user_count_ini + 1)
#
#         pwd_change_data = {
#             "new_password": anothers_data["password"][1:],
#             "current_password": anothers_data["password"],
#         }
#         response = self.client.post(
#             constants.TEST_USER_PWD_CHANGE,
#             data=pwd_change_data,
#             headers={
#                 "Authorization": f"Token {token_d[constants.AUTH_TOKEN_FIELD]}",
#             },
#         )
#         self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
#
#     def get_token(self, user_data) -> str:
#         response = self.client.post(
#             constants.TEST_USER_TOKEN_ON_URL,
#             data=user_data,
#         )
#         return json.loads(response.content)
