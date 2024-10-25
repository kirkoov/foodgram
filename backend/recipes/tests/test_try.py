# import json
# from http import HTTPStatus
# import pytest
#
# from backend.constants import TEST_RECIPE_PAGE_URL, TEST_TAG_PAGE_URL


# from recipes.tests.engine_class import Engine

# pytestmark = pytest.mark.skip  # Skip'em all from this module
# А для применения фикстуры ко всем тестам модуля, как и
# в случае с обычным маркером, нужно использовать зарезервированную глобальную
# переменную: pytestmark = pytest.mark.usefixtures('some_fixture').

# old_version = True


# class Engine:
#     """Класс двигателя."""
#
#     def __init__(self):
#         # При создании объекта двигателя он не запущен.
#         self.is_running = False


#
#
# def one_more(x):
#     return x + 1
#
#
# @pytest.mark.skip(reason="<reason>")  # commented off since the pytestmark is on
# def test_will_be_skipped():
#     assert True
#
#
# @pytest.mark.skipif(
#     "sys.version_info > (2, 7)", reason="Only for older Python versions"
# )
# def test_for_old_versions():
#     assert old_version is True
#
#
# @pytest.mark.xfail(reason="Let it fail, for training.")
# def test_false():
#     assert False


# @pytest.mark.parametrize(
#     "input_arg, expected_result",
#     [(4, 5), pytest.param(3, 5, marks=pytest.mark.xfail)],
#     ids=[
#         "First param",
#         "Second param",
#     ],
# )
# def test_one_more(input_arg, expected_result):
#     assert one_more(input_arg) == expected_result
#

#
# def test_engine_is_running(engine, start_engine):  # Вызываем обе фикстуры.
#     """Тест проверяет, работает ли двигатель."""
#     assert engine.is_running


# @pytest.mark.usefixtures("start_engine")
# def test_engine_is_running(engine):
#     """Тест проверяет, работает ли двигатель."""
#     assert engine.is_running


# # Now we use an autostarted fixture
# def test_engine_is_running(engine):
#     """Тест проверяет, работает ли двигатель."""
#     # print("test_engine_is_running")  # Выведем название теста.
#     assert engine.is_running


# Если определённую фикстуру нужно применить ко всем тестам класса, то
# применяется тот же декоратор @pytest.mark.usefixtures, только ставится он
# перед названием класса.


# def test_check_engine_class(engine):
#     """Тест проверяет класс объекта."""
#     # print("test_check_engine_class")  # Выведем название теста.
#     assert isinstance(engine, Engine)


# Default client fixtures from the pytest-django
# below


# def test_with_client(client):
#     response = client.get("/api/")
#     assert response.status_code == 401
#
#
# def test_closed_page(admin_client):
#     response = admin_client.get("/api/recipes/")
#     assert response.status_code == 200
#
#
# def test_with_authenticated_client(client, django_user_model):
#     user = django_user_model.objects.create(username="another_user")
#     client.force_login(user)
#     response = client.get("/api/users/1/")
#     assert response.status_code == 200


# @pytest.mark.django_db
# def test_home_availability_for_anonymous_user(client):
#     response = client.get(TEST_RECIPE_PAGE_URL)
#     # assert response.status_code == HTTPStatus.OK
#     print(json.loads(response.content))
