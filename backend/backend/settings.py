import os

from pathlib import Path
from dotenv import load_dotenv

from django.utils.translation import gettext_lazy as _


load_dotenv()


def show_toolbar(request):
    return True


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "secret-key")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split()

# DjDT
INTERNAL_IPS = ["127.0.0.1"]

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}

if DEBUG:
    import mimetypes

    mimetypes.add_type("application/javascript", ".js", True)


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "djoser",
    "corsheaders",
    "django_filters",
    "users.apps.UsersConfig",
    "recipes.apps.RecipesConfig",
    "api.apps.ApiConfig",
    "rosetta",
    "debug_toolbar",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
CORS_URLS_REGEX = r"^/api/.*$"

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql_psycopg2",
#         "NAME": os.getenv("POSTGRES_DB", "foodgram"),
#         "USER": os.getenv("POSTGRES_USER", "foodgram_user"),
#         "PASSWORD": os.getenv("POSTGRES_PASSWORD", "foodgram_password"),
#         "HOST": os.getenv("DB_HOST", ""),
#         "PORT": os.getenv("DB_PORT", 1234),
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db-test.sqlite3",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttribute"
        "SimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLength"
        "Validator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPassword"
        "Validator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPassword"
        "Validator",
    },
]


LANGUAGE_CODE = "ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_L10N = True
USE_TZ = True

AUTH_USER_MODEL = "users.CustomUser"

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumber"
    "Pagination",
    "PAGE_SIZE": 6,
}

LANGUAGES = (
    ("ru", _("Russian")),
    ("en", _("English")),
)
LOCALE_PATHS = [
    BASE_DIR / "locale/",
]

# MEDIA_ROOT = "/app/media/"
# STATIC_URL = "/static/django/"
# STATIC_ROOT = "/app/static_django/"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "collected_static"


DJOSER = {
    "HIDE_USERS": False,
    "LOGIN_FIELD": "email",
    "SERIALIZERS": {
        "user": "api.serializers.CustomUserSerializer",
        "current_user": "api.serializers.CustomUserSerializer",
    },
    "PERMISSIONS": {
        "user": ["djoser.permissions.CurrentUserOrAdminOrReadOnly"],
        "user_list": ["rest_framework.permissions.AllowAny"],
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

NUM_CHARS_FIRSTNAME = 150
NUM_CHARS_LASTNAME = 150
NUM_CHARS_EMAIL = 254

NUM_CHARS_MEALTIME_NAME = (
    NUM_CHARS_INGREDIENT_NAME
) = NUM_CHARS_RECIPE_NAME = 200
NUM_CHARS_MEALTIME_HEX = 7
NUM_CHARS_MEALTIME_SLUG = NUM_CHARS_MEASUREMENT_UNIT = 200

HEX_FIELD_REQ = "^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
SLUG_FIELD_REQ = "^[-a-zA-Z0-9_]+$"

MIN_COOKING_TIME_MINS = 1
MAX_COOKING_TIME_MINS = 525960  # = 365.25 days in min (e.g., for a cheese)

MIN_INGREDIENT_AMOUNT = 1
MAX_INGREDIENT_AMOUNT = 1000
