import pytest


@pytest.fixture(scope="module")
def get_standard_user_data():
    return {
        "url": "/api/users/",
        "token_url": "/api/auth/token/login/",
        "data": {
            "email": "standard@user.com",
            "username": "test_standard_uza",
            "first_name": "Test",
            "last_name": "Standard",
            "password": "wHat~Eva^_",
        },
    }


@pytest.fixture(scope="module")
def get_recipe_data():
    return {
        "url": "/api/recipes/",
        "data": {
            "ingredients": [{"id": 1123, "amount": 10}],
            "tags": [1, 2],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            "name": "Test recipe name",
            "text": "Cooking instructions for the test recipe name",
            "cooking_time": 1,
        },
    }
