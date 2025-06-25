PAGINATOR_NUM = 6
AUTH_TOKEN_FIELD = "auth_token"

# Test user data: BEGIN
TEST_NUM_USERS = 100
# Test user routes
TEST_USERS_PAGE_URL = "/api/users/"
TEST_USERS_TOKEN_URL = "/api/auth/token/"
TEST_USER_ME_PAGE_URL = TEST_USERS_PAGE_URL + "me/"

TEST_USERS_PER_PAGE_INT = 3

TEST_USERS_PER_PAGE_URL = TEST_USERS_PAGE_URL + (
    f"?limit={TEST_USERS_PER_PAGE_INT}"
)
TEST_USER_PAGE_PAGENUM = TEST_USERS_PAGE_URL + "?page=1"

TEST_USER_TOKEN_ON_URL = TEST_USERS_TOKEN_URL + "login/"
TEST_USER_TOKEN_OFF_URL = TEST_USERS_TOKEN_URL + "logout/"
TEST_USER_PWD_CHANGE = TEST_USERS_PAGE_URL + "set_password/"
TEST_USER_DATA = {
    "email": "vdoodkin@yandex.ru",
    "username": "vasya.doodkin",
    "first_name": "Вася",
    "last_name": "Doodkin",
    "password": "my_AwSeOm-pr$iOs",
}
TEST_USER_DATA_2 = {
    "email": "test_user@example.org",
    "username": "test.user",
    "first_name": "Test",
    "last_name": "User",
    "password": "Q_6~cwR-oL8y9Za",
}

# Test user content
TEST_USER_CONTENT_ITEMS = {
    "count": None,
    "next": None,
    "previous": None,
    "results": None,
}
TEST_USER_CONTENT_RESULTS_ITEMS = {
    "email": None,
    "id": 0,
    "username": None,
    "first_name": None,
    "last_name": None,
    "is_subscribed": False,
}

# Test user data: END


# Test recipe data: BEGIN
# Test recipe routes
TEST_RECIPE_PAGE_URL = "/api/recipes/"
TEST_TAG_PAGE_URL = "/api/tags/"

# Test recipe data: END


NUM_CHARS_USERNAME = 150
NUM_CHARS_FIRSTNAME = 150
NUM_CHARS_LASTNAME = 150
NUM_CHARS_EMAIL = 254

NUM_CHARS_INGREDIENT_NAME = NUM_CHARS_RECIPE_NAME = 200
NUM_CHARS_MEALTIME_HEX = 7
NUM_CHARS_MEALTIME_NAME = NUM_CHARS_MEALTIME_SLUG = (
    NUM_CHARS_MEASUREMENT_UNIT
) = 200

HEX_FIELD_REQ = "^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
SLUG_FIELD_REQ = "^[-a-zA-Z0-9_]+$"
USERNAME_FIELD_REQ = r"^[\w.@+-]+\\z$"

MIN_COOKING_TIME_MINS = 1
MAX_COOKING_TIME_MINS = 525960  # = 365.25 days in min (e.g., for a cheese)

MIN_INGREDIENT_AMOUNT = 1
MAX_INGREDIENT_AMOUNT = 1000

MAX_IMG_SIZE = 1  # Mb


TEST_SERVER_URL = "http://testserver"
TEST_LIMIT_LIST_USERS = 1

TEST_NUM_TAGS = 3
TEST_NUM_INGREDIENTS = 1000
TEST_NUM_RECIPES = 50
