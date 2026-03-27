"""
Base settings for Imali.

This file is the production-safe base for the settings package.
It should never be used directly — always use a specific environment settings file.

Settings package layout:
    settings/
    ├── __init__.py
    ├── base.py       ← you are here (production defaults)
    ├── dev.py        ← overrides for local development
    └── production.py ← overrides for production deployment

Usage:
    DJANGO_SETTINGS_MODULE=Imali.settings.dev
    DJANGO_SETTINGS_MODULE=Imali.settings.production

Docs: https://docs.djangoproject.com/en/stable/topics/settings/
"""

import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

load_dotenv()

# -----------------------------------------------------------------------------
# PATHS
# -----------------------------------------------------------------------------

# BASE_DIR resolves to the project root (three .parent calls because this file
# lives at Imali/settings/base.py inside the settings package).
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# -----------------------------------------------------------------------------
# CORE
# -----------------------------------------------------------------------------

ROOT_URLCONF = "Imali.urls"
WSGI_APPLICATION = "Imali.wsgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
APPEND_SLASH = True

# -----------------------------------------------------------------------------
# ENVIRONMENT
# -----------------------------------------------------------------------------

# SECRET_KEY must be set in the environment — never hardcode.
SECRET_KEY = os.getenv("SECRET_KEY")

# Defaults to False — production safe. dev.py should set DEBUG=True explicitly.
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# -----------------------------------------------------------------------------
# ADMINS
# Wired to the mail_admins logging handler below.
# Django will email these addresses on unhandled 500 errors in production
# when DEBUG=False and the email backend is configured.
# Docs: https://docs.djangoproject.com/en/stable/ref/settings/#admins
# -----------------------------------------------------------------------------

SITE_OWNER = os.getenv("SITE_OWNER")
ADMINS = [
    ("Site Owner", SITE_OWNER),
]

# -----------------------------------------------------------------------------
# APPLICATIONS
# -----------------------------------------------------------------------------

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    # --- Always present ---
    "whitenoise",
    "django_extensions",
    "health_check",

    # --- Uncomment if using DRF ---
    # "rest_framework",
    # "rest_framework.authtoken",  # only if using token auth

    # --- Uncomment if using CORS ---
    # "corsheaders",               # uv add django-cors-headers

    # --- Uncomment if using django-filter (DRF filtering) ---
    # "django_filters",            # uv add django-filter

    # --- Uncomment if using Celery + Redis ---
    # "django_celery_beat",        # uv add django-celery-beat (periodic tasks)
    # "django_celery_results",     # uv add django-celery-results (task result storage)
]

# IMPORTANT: The accounts app is a mandatory first step for any new project.
# Before running your first migration, create the accounts app and define
# CustomUser. AUTH_USER_MODEL cannot be changed after the initial migration
# without breaking the migration graph.
# See: https://docs.djangoproject.com/en/stable/topics/auth/customizing/#substituting-a-custom-user-model

LOCAL_APPS = [
    "accounts.apps.AccountsConfig",
    "core.apps.CoreConfig",  # abstract models, middleware, shared utilities
    # Add custom local apps here.
    "apps_directory.transactions"
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# -----------------------------------------------------------------------------
# AUTHENTICATION
# -----------------------------------------------------------------------------

# Must match the app declared in LOCAL_APPS above.
AUTH_USER_MODEL = "accounts.CustomUser"

# -----------------------------------------------------------------------------
# MIDDLEWARE
# -----------------------------------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # --- Uncomment if using CORS ---
    # "corsheaders.middleware.CorsMiddleware",  # must be before CommonMiddleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# -----------------------------------------------------------------------------
# DATABASE
# Docs: https://docs.djangoproject.com/en/stable/ref/settings/#databases
#
# Base is production-safe: ssl_require=True and conn_max_age for connection
# pooling. dev.py should override this entirely with a dev database URL
# and ssl_require=False.
# -----------------------------------------------------------------------------

DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True,
    )
}

# -----------------------------------------------------------------------------
# TEMPLATES
# Docs: https://docs.djangoproject.com/en/stable/ref/settings/#templates
# -----------------------------------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "Imali/templates"], # noqa
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# -----------------------------------------------------------------------------
# PASSWORD VALIDATION
# Docs: https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators
# -----------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -----------------------------------------------------------------------------
# INTERNATIONALISATION
# Docs: https://docs.djangoproject.com/en/stable/topics/i18n/
# -----------------------------------------------------------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Manila"
USE_I18N = True
USE_TZ = True

# -----------------------------------------------------------------------------
# STATIC FILES
# Docs: https://docs.djangoproject.com/en/stable/howto/static-files/
# -----------------------------------------------------------------------------

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"] # noqa
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# -----------------------------------------------------------------------------
# SECURITY
# All of these default to production-safe values.
# dev.py should override them to False to avoid redirect loops and cookie issues
# on localhost.
# Docs: https://docs.djangoproject.com/en/stable/topics/security/
# -----------------------------------------------------------------------------

# Redirect all HTTP requests to HTTPS.
SECURE_SSL_REDIRECT = True

# Prevent browsers from guessing content types (MIME sniffing).
SECURE_CONTENT_TYPE_NOSNIFF = True

# Tell browsers to only send cookies over HTTPS.
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS: tell browsers to enforce HTTPS for this many seconds.
# Start with a short value (300) and increase after confirming HTTPS is stable.
# Once set to a high value this is very difficult to reverse.
SECURE_HSTS_SECONDS = 300
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = False  # Only enable after HSTS is fully stable.

# Prevent this site from being embedded in an iframe on another origin.
X_FRAME_OPTIONS = "DENY"

# -----------------------------------------------------------------------------
# LOGGING
# Routes ERROR-level and above to the console and to mail_admins.
# mail_admins requires a working EMAIL_* configuration and ADMINS set above.
# Docs: https://docs.djangoproject.com/en/stable/topics/logging/
# -----------------------------------------------------------------------------

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console", "mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.server": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# -----------------------------------------------------------------------------
# HEALTH CHECK
# Docs: https://django-health-check.readthedocs.io/en/stable/
# -----------------------------------------------------------------------------

HEALTH_CHECK_TOKEN = os.getenv("HEALTH_CHECK_TOKEN")

# -----------------------------------------------------------------------------
# DJANGO REST FRAMEWORK (optional)
# Uncomment this block and add "rest_framework" to THIRD_PARTY_APPS above.
# Docs: https://www.django-rest-framework.org/api-guide/settings/
# -----------------------------------------------------------------------------

# REST_FRAMEWORK = {
#     "DEFAULT_AUTHENTICATION_CLASSES": [
#         "rest_framework.authentication.SessionAuthentication",
#         # "rest_framework.authentication.TokenAuthentication",
#     ],
#     "DEFAULT_PERMISSION_CLASSES": [
#         "rest_framework.permissions.IsAuthenticated",
#     ],
#     "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
#     "PAGE_SIZE": 20,
#     "DEFAULT_FILTER_BACKENDS": [
#         "django_filters.rest_framework.DjangoFilterBackend",
#         "rest_framework.filters.SearchFilter",
#         "rest_framework.filters.OrderingFilter",
#     ],
# }

# -----------------------------------------------------------------------------
# CORS (optional)
# Uncomment this block and add "corsheaders" to THIRD_PARTY_APPS above.
# Also uncomment CorsMiddleware in MIDDLEWARE above — it must sit before
# CommonMiddleware.
# Docs: https://github.com/adamchainz/django-cors-headers
# -----------------------------------------------------------------------------

# CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
# CORS_ALLOW_CREDENTIALS = False   # Set True only if sending cookies cross-origin.

# -----------------------------------------------------------------------------
# CELERY + REDIS (optional)
# Uncomment this block and add django-celery-beat / django-celery-results to
# THIRD_PARTY_APPS above if you need those features.
# Requires: uv add celery redis django-celery-beat django-celery-results
# Docs: https://docs.celeryq.dev/en/stable/userguide/configuration.html
# -----------------------------------------------------------------------------

# REDIS_URL = os.getenv("REDIS_URL")
#
# CELERY_BROKER_URL = REDIS_URL
# CELERY_RESULT_BACKEND = REDIS_URL
# CELERY_ACCEPT_CONTENT = ["json"]
# CELERY_TASK_SERIALIZER = "json"
# CELERY_RESULT_SERIALIZER = "json"
# CELERY_TIMEZONE = TIME_ZONE
# CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# -----------------------------------------------------------------------------
# CLOUDFLARE R2 STORAGE (optional)
# Uncomment this block when using R2 for file storage.
# Requires: uv add django-storages boto3
# Docs: https://django-storages.readthedocs.io/en/stable/backends/amazon-S3.html
#
# NOTE: R2 uses two buckets with different access patterns:
#   - Public bucket: profile pictures, served via CDN (no signing needed).
#   - Private bucket: receipts and exports, served via pre-signed URLs.
# -----------------------------------------------------------------------------

# AWS_S3_ENDPOINT_URL = os.getenv("R2_ENDPOINT_URL")     # https://<accountid>.r2.cloudflarestorage.com
# AWS_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
# AWS_S3_SIGNATURE_VERSION = "s3v4"
# AWS_QUERYSTRING_AUTH = False      # Set True for the private bucket (pre-signed URLs).
# AWS_S3_FILE_OVERWRITE = False

# Public bucket (CDN-served assets):
# AWS_STORAGE_BUCKET_NAME = os.getenv("R2_PUBLIC_BUCKET_NAME")
# AWS_S3_CUSTOM_DOMAIN = os.getenv("R2_PUBLIC_CDN_DOMAIN")  # your cdn.example.com
# DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# Private bucket (pre-signed URL assets):
# PRIVATE_BUCKET_NAME = os.getenv("R2_PRIVATE_BUCKET_NAME")
