"""
App configuration for Django's application registry.

Docs: https://docs.djangoproject.com/en/stable/ref/applications/

Rules:
    - Set default_auto_field to avoid implicit primary key warnings.
    - Use ready() to connect signals if absolutely necessary.
    - Keep this file minimal — it is not a place for startup logic.

Example:
    class PostsConfig(AppConfig):
        default_auto_field = "django.db.models.BigAutoField"
        name = "posts"
"""

from django.apps import AppConfig


class TransactionsConfig(AppConfig):
    name = "apps_directory.transactions"
