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
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localHHost").split()


if not DEBUG:
    # For DjDT
    import mimetypes

    mimetypes.add_type("application/javascript", ".js", True)
    INTERNAL_IPS = ["127.0.0.1"]

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": show_toolbar,
    }


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
    "django_cleanup.apps.CleanupConfig",
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

# For a Docker deploy, GitHub-based
CSRF_TRUSTED_ORIGINS = [
    "https://foodgram.zapto.org",
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


MEDIA_URL = "/media/"

# if DEBUG:
#     # Local dev case
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.sqlite3",
#             "NAME": "db.sqlite3",
#         }
#     }
#     MEDIA_ROOT = BASE_DIR / "media"
#     STATIC_URL = "static/"
#     STATIC_ROOT = BASE_DIR / "collected_static"
# else:
# Docker/orchestration case
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        # Local legacy
        # "ENGINE": "django.db.backends.postgresql_psycopg2" :
        # POSTGRES_DB=postgres
        # POSTGRES_USER=postgres
        # POSTGRES_PASSWORD=foodgram_password
        # DB_NAME=postgres
        "NAME": os.getenv("POSTGRES_DB", "foodgram"),
        "USER": os.getenv("POSTGRES_USER", "foodgram_user"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "foodgram_password"),
        "HOST": os.getenv("DB_HOST", ""),
        "PORT": os.getenv("DB_PORT", "1234"),
    }
}
MEDIA_ROOT = "/app/media/"  # type: ignore[assignment]
STATIC_URL = "/static/django/"
STATIC_ROOT = "/app/static_django/"  # type: ignore[assignment]


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


LANGUAGE_CODE = "en"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_L10N = True
USE_TZ = True

AUTH_USER_MODEL = "users.User"

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


DJOSER = {
    "HIDE_USERS": False,
    "LOGIN_FIELD": "email",
    "SERIALIZERS": {
        "user": "api.serializers.UserSerializer",
        "current_user": "api.serializers.UserSerializer",
    },
    "PERMISSIONS": {
        "user": ["djoser.permissions.CurrentUserOrAdminOrReadOnly"],
        "user_list": ["rest_framework.permissions.AllowAny"],
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
