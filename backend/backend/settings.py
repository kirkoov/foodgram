from datetime import timedelta
from pathlib import Path

from django.utils.translation import gettext_lazy as _


def show_toolbar(request):
    return True


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = (
    "django-insecure-tzt1(#hb_0%wb!!12@1$h#-4a36=)d4=(a3cyt%+hgf$x7o$hc"
)

DEBUG = True

ALLOWED_HOSTS = ["*"]

# For DjDT
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
    "djoser",
    "users.apps.UsersConfig",
    "recipes.apps.RecipesConfig",
    "debug_toolbar",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
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


REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=100),
    "AUTH_HEADER_TYPES": ("Bearer",),
}


LANGUAGE_CODE = "en"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ("en", _("English")),
    ("ru", _("Russian")),
)

LOCALE_PATHS = [
    BASE_DIR / "locale/",
]


STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.CustomUser"

NUM_CHARS_FIRSTNAME = 50
NUM_CHARS_LASTNAME = 50
NUM_CHARS_EMAIL = 254

NUM_CHARS_MEALTIME = 200
NUM_CHARS_MEALTIME_HEX = 16
NUM_CHARS_MEALTIME_SLUG = 16
