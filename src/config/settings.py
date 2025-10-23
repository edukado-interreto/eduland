import os
import sys
from pathlib import Path

from toml_decouple import config


def mod(pkg: str, modules: list[str]) -> list[str]:
    return [".".join([t for t in [pkg, module] if t]) for module in modules]


CONFIG_DIR = Path(__file__).absolute().parent
BASE_DIR = CONFIG_DIR.parent
PROJECT_DIR = BASE_DIR.parent

SECRET_KEY = config.SECRET_KEY
DEBUG = config.DEBUG
TESTING = "test" in sys.argv or "PYTEST_VERSION" in os.environ

if not DEBUG:
    ALLOWED_HOSTS = config.ALLOWED_HOSTS

DJANGO_CONTRIB_APPS = [
    "admin",
    "auth",
    "contenttypes",
    "sessions",
    "messages",
    "staticfiles",
]
WAGTAIL_APPS = [
    "contrib.forms",
    "contrib.redirects",
    "embeds",
    "sites",
    "users",
    "snippets",
    "documents",
    "images",
    "search",
    "admin",
    "",
]
PROJECT_APPS = ["core", "education", "home", "search"]

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "wagtail_localize",
    "wagtail_localize.locales",
    *mod("wagtail", WAGTAIL_APPS),
    "modelcluster",
    "taggit",
    "django_filters",
    "django_extensions",
    *mod("django.contrib", DJANGO_CONTRIB_APPS),
    "django_ftl.apps.DjangoFtlConfig",
    *mod("apps", PROJECT_APPS),
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django_ftl.middleware.activate_from_request_language_code",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG}

if not TESTING:
    INSTALLED_APPS = [
        *INSTALLED_APPS,
        "debug_toolbar",
    ]
    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        *MIDDLEWARE,
    ]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "config.context_processors.app",
                "config.context_processors.fluent",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config.PROJECT,
        "USER": config.PROJECT,
        "PASSWORD": config.DB_PASSWORD,
        "HOST": "postgres",
        "PORT": "5432",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

WAGTAIL_SITE_NAME = config.PROJECT

# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = config.HOST

# Allowed file extensions for documents in the document library.
# This can be omitted to allow all files, but note that this may present a security risk
# if untrusted users are allowed to upload files -
# see https://docs.wagtail.org/en/stable/advanced_topics/deploying.html#user-uploaded-files
WAGTAILDOCS_EXTENSIONS = [
    "csv",
    "docx",
    "key",
    "odt",
    "pdf",
    "pptx",
    "rtf",
    "txt",
    "xlsx",
    "zip",
]

USE_TZ, TIME_ZONE = True, "Europe/Bratislava"

LANGUAGE_CODE = "en"
LANGUAGE_COOKIE_NAME = "lang"
USE_I18N = WAGTAIL_I18N_ENABLED = True
WAGTAIL_CONTENT_LANGUAGES = LANGUAGES = [
    ("fr", "French"),
    ("sk", "Slovak"),
    ("en", "English"),
    ("eo", "Esperanto"),
]

WHITENOISE_ROOT = BASE_DIR / "public"
STATICFILES_DIRS = [BASE_DIR / "public" / "static"]
STATIC_URL = "static/"
MEDIA_ROOT = PROJECT_DIR / "uploads/"
MEDIA_URL = "uploads/"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
