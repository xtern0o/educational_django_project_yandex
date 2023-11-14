import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _
from dotenv.main import load_dotenv

__all__ = []


load_dotenv()


def load_bool_env(name, default):
    env_value = os.getenv(name, str(default)).lower()
    return env_value in ("true", "1", "yes", "y", "t")


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "NO_KEY")

DEBUG = load_bool_env("DJANGO_DEBUG", False)

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",")

ALLOW_REVERSE = load_bool_env("DJANGO_ALLOW_REVERSE", False)

# Application definition

INSTALLED_APPS = [
    "about.apps.AboutConfig",
    "catalog.apps.CatalogConfig",
    "download.apps.DownloadConfig",
    "feedback.apps.FeedbackConfig",
    "homepage.apps.HomepageConfig",
    "users.apps.UsersConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "sorl.thumbnail",
    "django_cleanup.apps.CleanupConfig",
    "widget_tweaks",
    "ckeditor",
]

INTERNAL_IPS = [
    "127.0.0.1",
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
    "lyceum.middleware.ReverseRussianWordsMiddleware",
]

if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")


ROOT_URLCONF = "lyceum.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "lyceum.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation."
        "UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "NumericPasswordValidator",
    },
]

LOGIN_URL = "/auth/login"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/auth/login"

if DEBUG:
    DEFAULT_USER_IS_ACTIVE = True
else:
    DEFAULT_USER_IS_ACTIVE = load_bool_env("DEFAULT_USER_IS_ACTIVE", False)


LANGUAGE_CODE = "ru"
LANGUAGES = [
    ("ru", _("Russian")),
    ("en", _("English")),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_ROOT = BASE_DIR / "static"
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static_dev",
]

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CKEDITOR_CONFIGS = {
    "default": {
        "height": 300,
        "width": 600,
        "toolbar": "Custom",
        "toolbar_Custom": [
            [
                "Undo",
                "Redo",
                "-",
                "Font",
                "FontSize",
                "-",
                "Bold",
                "Italic",
                "Underline",
            ],
            [
                "JustifyLeft",
                "JustifyCenter",
                "JustifyRight",
                "JustifyBlock",
            ],
        ],
    },
}

EMAIL_ADDRESS = os.getenv("DJANGO_MAIL", "NO-MAIL")
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "send_mail"

LINK_EXPIRATION = int(os.getenv("LINK_EXPIRATION", 12))
