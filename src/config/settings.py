import os
import sys
from pathlib import Path
from typing import Any, cast

from toml_decouple import config


def mod(pkg: str, modules: list[str]) -> list[str]:
    return [".".join([t for t in [pkg, module] if t]) for module in modules]


SRC_DIR = Path(__file__).absolute().parent.parent
PROJECT_DIR = SRC_DIR.parent

SECRET_KEY = config("SECRET_KEY", "NESEKURA")
DEBUG = config("DEBUG", False)
TESTING = "test" in sys.argv or "PYTEST_VERSION" in os.environ

_DEFAULT_HOST = "127.0.0.1"
ALLOWED_HOSTS = cast(
    list[str], config("ALLOWED_HOSTS", [config("HOST", _DEFAULT_HOST)])
)
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    default=[f"https://{h}" for h in ALLOWED_HOSTS],
)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

_DJANGO_CONTRIB_APPS = [
    "admin",
    "auth",
    "contenttypes",
    "sessions",
    "messages",
    "postgres",
    "staticfiles",
]
_WAGTAIL_APPS = [
    "contrib.forms",
    "contrib.redirects",
    "embeds",
    "sites",
    "users",
    "snippets",
    "documents",
    # "images",  replaced by apps.core.apps.CustomImagesAppConfig
    "search",
    "admin",
    "",
]
_PROJECT_APPS = ["core", "education", "home", "search"]

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "wagtail_localize_intentional_blanks",
    "wagtail_localize",
    "wagtail_localize.locales",
    *mod("wagtail", _WAGTAIL_APPS),
    "modelcluster",
    "taggit",
    "django_filters",
    "django_extensions",
    *mod("django.contrib", _DJANGO_CONTRIB_APPS),
    "django_ftl.apps.DjangoFtlConfig",
    "django_vite",
    *mod("apps", _PROJECT_APPS),
    "apps.core.apps.CustomImagesAppConfig",
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

# Django Debug Toolbar
if DEBUG and not TESTING:
    INSTALLED_APPS = [*INSTALLED_APPS, "debug_toolbar"]
    MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware", *MIDDLEWARE]
    DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG}

# CORS headers for Vite dev mode
if DEBUG:
    INSTALLED_APPS = ["corsheaders", *INSTALLED_APPS]
    MIDDLEWARE = ["corsheaders.middleware.CorsMiddleware", *MIDDLEWARE]
    CORS_ALLOWED_ORIGINS = [
        "http://eduland.localhost:5173",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://eduland.localhost:5173",
        "https://localhost:5173",
        "https://127.0.0.1:5173",
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

CACHE_TIMEOUT_SEC = 5 if DEBUG else 2 * 3600  # 2 hours

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("PROJECT", "eduland"),
        "USER": config("PROJECT", "eduland"),
        "PASSWORD": config("DB_PASSWORD", "NESEKURA"),
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

WAGTAIL_SITE_NAME = config("PROJECT", "eduland")

# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = config("HOST", _DEFAULT_HOST)

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

WAGTAILEMBEDS_RESPONSIVE_HTML = True
WAGTAILDOCS_SERVE_METHOD = "direct"
WAGTAILDOCS_INLINE_CONTENT_TYPES = ["application/pdf"]

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

WHITENOISE_ROOT = SRC_DIR / "public"
STATICFILES_DIRS = [SRC_DIR / "public" / "static"]
STATIC_URL = "static/"
STATIC_ROOT = PROJECT_DIR / "staticfiles/"
MEDIA_ROOT = PROJECT_DIR / "uploads/"
MEDIA_URL = "uploads/"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

DJANGO_VITE = {
    "default": {
        "manifest_path": SRC_DIR / "public/static/vue/assets/manifest.json",
        "static_url_prefix": "vue",
        "dev_mode": config("DJANGO_VITE_DEV_MODE", False),
        "dev_server_host": config("HOST", _DEFAULT_HOST),
        "dev_server_port": "443",  # Overrides 5173
        "dev_server_protocol": "https",  # Overrides http
    }
}


LOGGING: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": [],  # ["require_debug_true"]
            "class": "logging.StreamHandler",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "mail_admins"],
            "level": "INFO",
        },
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
