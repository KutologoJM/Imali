"""
Celery application configuration for Imali.

This file must live in the project configuration package (next to settings/).

To activate Celery in this project:
    1. Uncomment the Celery + Redis block in settings/base.py.
    2. Add the relevant packages to pyproject.toml and run `uv sync`.
    3. Uncomment the code in this file.
    4. Add the import in Imali/__init__.py (see bottom of this file).

Running a worker locally:
    uv run celery -A Imali worker -l info

Running the beat scheduler (periodic tasks):
    uv run celery -A Imali beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

Docs: https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html
"""

# import os
# from celery import Celery
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Imali.settings.production")
#
# app = Celery("Imali")
#
# # Load CELERY_* settings from Django settings.
# app.config_from_object("django.conf:settings", namespace="CELERY")
#
# # Autodiscover tasks in all installed apps (looks for tasks/__init__.py).
# app.autodiscover_tasks()


# -----------------------------------------------------------------------------
# Add the following to Imali/__init__.py to ensure the Celery app
# is loaded when Django starts, so shared_task decorators work correctly:
#
#   from .celery import app as celery_app
#   __all__ = ["celery_app"]
# -----------------------------------------------------------------------------
