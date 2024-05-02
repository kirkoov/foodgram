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

PAGINATOR_NUM = 6

TEST_NUM_USERS = 100
TEST_SERVER_URL = "http://testserver"
TEST_LIMIT_LIST_USERS = 1

TEST_NUM_TAGS = 5
TEST_NUM_INGREDIENTS = 2000
TEST_NUM_RECIPES = 100
