from itertools import product
from pathlib import Path

from dj_database_url import parse as db_url_parse
from toml_decouple import config

from .error_tracking import setup_bugsink
from .logging import DEV_LOGGING, PROD_LOGGING
from .utils import Environment, django_vite_dev_mode, mod

PROJECT_DIR = Path(__file__).absolute().parent.parent

SECRET_KEY = config("SECRET_KEY", "NESEKURA")
DEBUG = config("DEBUG", False)
ENVIRONMENT = Environment.init(config, DEBUG)

HOSTNAME = config("HOSTNAME", "127.0.0.1")
HOST = config("HOST", "0.0.0.0")
PORT = config("PORT", 8000)
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    list({HOSTNAME, "django", "localhost", "127.0.0.1", "0.0.0.0"}),
)

CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    default=[f"https://{h}" for h in ALLOWED_HOSTS],
)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 31536000 if ENVIRONMENT.deployed else 0
SESSION_COOKIE_SECURE = CSRF_COOKIE_SECURE = ENVIRONMENT.deployed


### INSTALLED_APPS ###

_DJANGO_CONTRIB_APPS = [
    "admin",
    "auth",
    "contenttypes",
    "sessions",
    "messages",
    "postgres",
    "sitemaps",
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
    "wagtail_localize_intentional_blanks",
    "wagtail_localize",
    "wagtail_localize.locales",
    "wagtailmenus",
    *mod("wagtail", _WAGTAIL_APPS),
    "modelcluster",
    "taggit",
    "django_filters",
    "django_extensions",
    *mod("django.contrib", _DJANGO_CONTRIB_APPS),
    "django_ftl.apps.DjangoFtlConfig",
    "django_vite",
    "django_rsgi",
    *mod("apps", _PROJECT_APPS),
    "apps.core.apps.CustomImagesAppConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
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

if ENVIRONMENT == Environment.DEV:
    # Django Debug Toolbar
    INSTALLED_APPS = [*INSTALLED_APPS, "debug_toolbar"]
    MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware", *MIDDLEWARE]
    DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG}

    if django_vite_dev_mode(ENVIRONMENT):
        # CORS headers for Vite dev mode
        INSTALLED_APPS = ["corsheaders", *INSTALLED_APPS]
        MIDDLEWARE = ["corsheaders.middleware.CorsMiddleware", *MIDDLEWARE]
        CORS_ALLOWED_ORIGINS = [
            f"http{secure}://{host}:5173"
            for secure, host in product(("", "s"), ALLOWED_HOSTS)
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
                "wagtailmenus.context_processors.wagtailmenus",
                "config.context_processors.app",
                "config.context_processors.fluent",
            ],
        },
    },
]

if "DATABASE_URL" in config:
    DATABASES = {
        "default": {
            **config("DATABASE_URL", to=db_url_parse),
            "PASSWORD": config("POSTGRES_PASSWORD"),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": f"django.contrib.auth.password_validation.{cls}"}
    for cls in [
        "UserAttributeSimilarityValidator",
        "MinimumLengthValidator",
        "CommonPasswordValidator",
        "NumericPasswordValidator",
    ]
]

CACHE_TIMEOUT_SEC = 5 if DEBUG else 48 * 3600  # 48 hours

WAGTAIL_SITE_NAME = f"EduLand {ENVIRONMENT.display_name()}"

# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {"default": {"BACKEND": "wagtail.search.backends.database"}}

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = f"https://{HOSTNAME}"

# Allowed file extensions for documents in the document library.
# This can be omitted to allow all files, but note that this may present a security risk
# if untrusted users are allowed to upload files -
# see https://docs.wagtail.org/en/stable/advanced_topics/deploying.html#user-uploaded-files
WAGTAILDOCS_EXTENSIONS = ["csv", "docx", "odt", "pdf", "pptx", "rtf", "xlsx", "zip"]

WAGTAILEMBEDS_RESPONSIVE_HTML = True  # CSS class .responsive-object
WAGTAILDOCS_SERVE_METHOD = "direct"
WAGTAILDOCS_INLINE_CONTENT_TYPES = ["application/pdf"]

TIME_ZONE = "Europe/Bratislava"

LANGUAGE_CODE = "en"
LANGUAGE_COOKIE_NAME = "lang"
WAGTAIL_I18N_ENABLED = True
WAGTAIL_CONTENT_LANGUAGES = LANGUAGES = [
    ("fr", "French"),
    ("sk", "Slovak"),
    ("en", "English"),
    ("eo", "Esperanto"),
]

PUBLIC_ROOT = PROJECT_DIR / "config/public"
STATICFILES_DIRS = [PROJECT_DIR / "config/static"]
STATIC_URL = "static/"
STATIC_ROOT = PROJECT_DIR / "staticfiles"
MEDIA_ROOT = PROJECT_DIR / "uploads"
MEDIA_URL = "uploads/"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}

DJANGO_VITE = {
    "default": {
        "manifest_path": STATICFILES_DIRS[0] / "vue/assets/manifest.json",
        "static_url_prefix": "vue",
        "dev_mode": django_vite_dev_mode(ENVIRONMENT),
        "dev_server_host": HOSTNAME,
        "dev_server_port": "443",  # Overrides 5173
        "dev_server_protocol": "https",  # Overrides http
    }
}

LOGGING = DEV_LOGGING

if ENVIRONMENT.deployed:
    LOGGING = PROD_LOGGING
    setup_bugsink(config)
