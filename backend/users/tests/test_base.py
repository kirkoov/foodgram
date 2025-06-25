from http import HTTPStatus

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from backend import constants

User = get_user_model()


class UserAuthTestMixin(APITestCase):
    """
    A mixin providing common user creation and authentication utilities
    for Django REST Framework tests.
    """

    # Store dummy data for a user to be created and authenticated
    # This data should be unique enough not to conflict with other setup.
    # Note: Using a dict copy here to ensure each test method gets a fresh copy
    # if modified.
    DUMMY_AUTH_DATA = dict(constants.TEST_USER_DATA)

    def _create_user(self, user_data=None):
        """
        Helper to create a user. If no data is provided, creates a user
        based on DUMMY_AUTH_DATA.
        """
        if user_data is None:
            user_data = self.DUMMY_AUTH_DATA

        # Ensure user_data is a mutable copy if it's being modified
        user_data_copy = dict(user_data)

        # The password here is plain-text, Django will hash it.
        user = User.objects.create_user(
            username=user_data_copy.get("username"),
            email=user_data_copy.get("email"),
            password=user_data_copy.get("password"),
            first_name=user_data_copy.get("first_name"),
            last_name=user_data_copy.get("last_name"),
        )
        return user, user_data_copy

    def _get_auth_token(self, email=None, password=None):
        """
        Helper to authenticate a user and retrieve their authentication token.
        Assumes token authentication is enabled in DRF settings.
        """
        login_data = {
            "email": email if email else self.DUMMY_AUTH_DATA["email"],
            "password": (
                password if password else self.DUMMY_AUTH_DATA["password"]
            ),
        }
        response = self.client.post(
            constants.TEST_USER_TOKEN_ON_URL,
            data=login_data,
            format="json",
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        return response.data[constants.AUTH_TOKEN_FIELD]

    def _get_auth_headers(self, email=None, password=None):
        """
        Helper to get authentication headers for a user.
        """
        token = self._get_auth_token(email, password)
        return {"Authorization": f"Token {token}"}
