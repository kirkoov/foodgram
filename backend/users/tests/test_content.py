# import json
# import random
#
# from django.contrib.auth import get_user_model
# from django.test import TestCase
# from users.validators import validate_username_field
#
# from backend import constants
#
# User = get_user_model()
#
#
# class TestContent(TestCase):
#     TOTAL = random.randint(1, constants.TEST_NUM_USERS)
#
#     @classmethod
#     def setUpTestData(cls):
#         User.objects.bulk_create(
#             User(
#                 username=f"{constants.TEST_USER_DATA_2['username']}{idx}",
#                 first_name=f"{constants.TEST_USER_DATA_2['first_name']}{idx}",
#                 last_name=f"{constants.TEST_USER_DATA_2['last_name']}{idx}",
#                 email=f"{constants.TEST_USER_DATA_2['email']}{idx}",
#                 password=f"{constants.TEST_USER_DATA_2['password']}{idx}",
#             )
#             for idx in range(cls.TOTAL)
#         )
#
#     def test_user_count(self):
#         self.assertEqual((u_count := User.objects.count()), self.TOTAL)
#         response = self.client.get(constants.TEST_USERS_PAGE)
#         # fmt: off
#         self.assertEqual(
#             len((user_d := json.loads(response.content))["results"]),
#             constants.PAGINATOR_NUM
#         )
#         self.assertEqual(user_d["count"], u_count)
#
#     def test_user_list_structure_paging(self):
#         response = self.client.get(constants.TEST_USERS_PAGE)
#         self.assertEqual(
#             (users_d := json.loads(response.content)).keys(),
#             constants.TEST_USER_CONTENT_ITEMS.keys(),
#         )
#         self.assertIn("?page=2", users_d["next"])
#         self.assertIsNone(users_d["previous"])
#
#         for u_d in users_d["results"]:
#             self.assertEqual(
#                 u_d.keys(), constants.TEST_USER_CONTENT_RESULTS_ITEMS.keys()
#             )
#             self.assertTrue(len(u_d["username"]) <= constants.NUM_CHARS_USERNAME)
#             self.assertTrue(validate_username_field(u_d["username"]))
#             self.assertTrue(len(u_d["first_name"]) <= constants.NUM_CHARS_FIRSTNAME)
#             self.assertTrue(len(u_d["last_name"]) <= constants.NUM_CHARS_LASTNAME)
#             self.assertTrue(len(u_d["email"]) <= constants.NUM_CHARS_EMAIL)
#
#     # def test_user_list_limit(self):
#     #     response = self.client.get(constants.TEST_USER_PAGE_LIMIT)
#     #     self.assertEqual(
#     #         (users_d := json.loads(response.content)).keys(),
#     #         constants.TEST_USER_CONTENT_ITEMS.keys(),
#     #     )
#     #     # fmt: off
#     #     self.assertIn(
#     #         f"page={constants.TEST_USER_PAGE_LIMIT_INT + 1}",
#     #         users_d["next"]
#     #     )
#     #     # fmt: off
#     #     self.assertIn(
#     #         f"limit={constants.TEST_USER_PAGE_LIMIT_INT}",
#     #         users_d["next"]
#     #     )
#
#     # def test_signup_user(self):
#     #     # fmt: off
#     #     response = self.client.post(
#     #         constants.TEST_USERS_PAGE,
#     #         data=constants.TEST_USER_DATA,
#     #     )
#     #     compare_d = constants.TEST_USER_DATA
#     #     self.assertIn("id", (resp_d := json.loads(response.content)))
#     #     compare_d["id"] = resp_d["id"]
#     #     del compare_d["password"]
#     #     self.assertEqual(compare_d, resp_d)
#
#     def test_fail_signup_user(self):
#         fail_field = "email"
#         fail_data = constants.TEST_USER_DATA_2
#         fail_data[fail_field] = "invalid@email"
#         response = self.client.post(
#             constants.TEST_USERS_PAGE,
#             data=fail_data,
#         )
#         self.assertIn(fail_field, json.loads(response.content))
#
#     # @staticmethod
#     # def delete_test_users():
#     #     User.objects.all().delete()
#     #
#     # @classmethod
#     # def tearDownClass(cls):
#     #     cls.delete_test_users()
