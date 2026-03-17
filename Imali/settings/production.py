"""
Production settings for Imali.

Inherits all production-safe defaults from base.py. Only add settings here
that require real production credentials or differ from base.py defaults.

Usage:
    DJANGO_SETTINGS_MODULE=Imali.settings.production

Docs: https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
"""

from .base import *  # noqa: F403

# -----------------------------------------------------------------------------
# SECURITY
# base.py sets SECURE_HSTS_SECONDS = 300 as a safe starting value.
# Once you have confirmed HTTPS is fully stable and all subdomains are covered,
# increase this progressively: 300 → 3600 → 86400 → 31536000.
# Setting a high value is very difficult to reverse — browsers will enforce it
# for the full duration even after you change the header.
# Docs: https://docs.djangoproject.com/en/stable/ref/settings/#secure-hsts-seconds
# -----------------------------------------------------------------------------

SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", 300))  # noqa: F405

# Uncomment once HSTS is fully stable and all subdomains serve HTTPS.
# SECURE_HSTS_PRELOAD = True

# -----------------------------------------------------------------------------
# DATABASE
# Inherits ssl_require=True and conn_max_age=600 from base.py.
# DATABASE_URL should be set in the production environment — never hardcoded.
# -----------------------------------------------------------------------------

# No override needed — base.py database config is production-ready as-is.
# Ensure DATABASE_URL is set in your production environment.

# -----------------------------------------------------------------------------
# CACHE
# Uses Redis if REDIS_URL is configured, otherwise falls back to the database
# cache. Database cache requires: python manage.py createcachetable
# Docs: https://docs.djangoproject.com/en/stable/topics/cache/
# -----------------------------------------------------------------------------

_REDIS_URL = os.getenv("REDIS_URL")  # noqa: F405

if _REDIS_URL:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": _REDIS_URL,
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.db.DatabaseCache",
            "LOCATION": "cache_table",
            # Run: python manage.py createcachetable
        }
    }

# -----------------------------------------------------------------------------
# EMAIL
# Sends real email via SMTP in production.
# All values must be set in the production environment.
# Docs: https://docs.djangoproject.com/en/stable/topics/email/#smtp-backend
# -----------------------------------------------------------------------------

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST")  # noqa: F405
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))  # noqa: F405
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")  # noqa: F405
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")  # noqa: F405
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"  # noqa: F405
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")  # noqa: F405
SERVER_EMAIL = DEFAULT_FROM_EMAIL  # Used by mail_admins logging handler.

# -----------------------------------------------------------------------------
# SENTRY (optional)
# Uncomment to enable error tracking and performance monitoring in production.
# Requires: uv add sentry-sdk
# Docs: https://docs.sentry.io/platforms/python/integrations/django/
# -----------------------------------------------------------------------------

# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration
# from sentry_sdk.integrations.celery import CeleryIntegration  # if using Celery
# from sentry_sdk.integrations.redis import RedisIntegration    # if using Redis
#
# sentry_sdk.init(
#     dsn=os.getenv("SENTRY_DSN"),
#     integrations=[
#         DjangoIntegration(),
#         # CeleryIntegration(),
#         # RedisIntegration(),
#     ],
#     # Percentage of transactions to send for performance monitoring (0.0 to 1.0).
#     traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0.1")),
#     send_default_pii=False,  # Never send personally identifiable information.
# )