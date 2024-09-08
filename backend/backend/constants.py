# Test user data
TEST_USERS_PAGE = "/api/users/"
TEST_USERS_TOKEN = "/api/auth/token/"
TEST_USER_OWN_PAGE = TEST_USERS_PAGE + "me/"
TEST_USER_PAGE_PAGENUM = TEST_USERS_PAGE + "?page=1"
TEST_USER_PAGE_LIMIT = TEST_USERS_PAGE + "?limit=1"
TEST_USER_TOKEN_ON = TEST_USERS_TOKEN + "login/"
TEST_USER_TOKEN_OFF = TEST_USERS_TOKEN + "logout/"

TEST_USER_DATA = {
    "email": "vpupkin@yandex.ru",
    "username": "vasya.pupkin",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "password": "my_AwSeOm-pr$iOs",
}
TEST_USER_DATA_2 = {
    "email": "test.user@aha.org",
    "username": "test.user",
    "first_name": "Test",
    "last_name": "User",
    "password": "Q_6wR-oL8y9Za",
}

NUM_CHARS_USERNAME = 150
NUM_CHARS_FIRSTNAME = 150
NUM_CHARS_LASTNAME = 150
NUM_CHARS_EMAIL = 254

NUM_CHARS_INGREDIENT_NAME = NUM_CHARS_RECIPE_NAME = 200
NUM_CHARS_MEALTIME_HEX = 7
NUM_CHARS_MEALTIME_NAME = NUM_CHARS_MEALTIME_SLUG = NUM_CHARS_MEASUREMENT_UNIT = 200

HEX_FIELD_REQ = "^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
SLUG_FIELD_REQ = "^[-a-zA-Z0-9_]+$"
USERNAME_FIELD_REQ = r"^[\w.@+-]+\\z$"

MIN_COOKING_TIME_MINS = 1
MAX_COOKING_TIME_MINS = 525960  # = 365.25 days in min (e.g., for a cheese)

MIN_INGREDIENT_AMOUNT = 1
MAX_INGREDIENT_AMOUNT = 1000

MAX_IMG_SIZE = 1  # Mb

PAGINATOR_NUM = 6

TEST_NUM_USERS = 100
TEST_SERVER_URL = "http://testserver"
TEST_LIMIT_LIST_USERS = 1

TEST_NUM_TAGS = 5
TEST_NUM_INGREDIENTS = 1000
TEST_NUM_RECIPES = 50
