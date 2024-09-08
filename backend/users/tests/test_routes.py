from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase

from backend import constants

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(**constants.TEST_USER_DATA)

    def test_users_pages_availability(self):
        urls = (
            (constants.TEST_USERS_PAGE, None, HTTPStatus.OK),
            (constants.TEST_USER_PAGE_PAGENUM, None, HTTPStatus.OK),
            (constants.TEST_USER_PAGE_LIMIT, None, HTTPStatus.OK),
            (constants.TEST_USERS_PAGE, self.user.id, HTTPStatus.OK),
            (constants.TEST_USERS_PAGE, User.objects.count() + 1, HTTPStatus.NOT_FOUND),
            (constants.TEST_USER_OWN_PAGE, None, HTTPStatus.UNAUTHORIZED),
        )
        for url, args, status in urls:
            # url = reverse(url, args=args)
            with self.subTest(url=url):
                if args is None:
                    response = self.client.get(url)
                else:
                    response = self.client.get(f"{url}{args}/")
                self.assertEqual(response.status_code, status)

    def test_user_signup_and_see_own_page(self):
        ...
        # response = self.client.get(constants.TEST_USER_OWN_PAGE)
        # self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_fail_signup_user(self):
        # fmt: off
        fail_data = constants.TEST_USER_DATA
        fail_data["email"] = "invalid@email"
        response = self.client.post(
            constants.TEST_USERS_PAGE,
            data=fail_data,
            # follow_redirects=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_signup_user(self):
        user_count_ini = User.objects.count()
        # fmt: off
        response = self.client.post(
            constants.TEST_USERS_PAGE,
            data=constants.TEST_USER_DATA_2,
        )
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        user_count = User.objects.count()
        self.assertEqual(user_count, user_count_ini + 1)

        # # login with new user
        # response = self.client.post('/auth/login', data={
        #     'username': 'alice',
        #     'password': 'foo',
        # }, follow_redirects=True)
        # assert response.status_code == 200
        # html = response.get_data(as_text=True)
        # assert 'Hi, alice!' in html
