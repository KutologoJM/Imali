"""
Root pytest configuration.

This file's sole job is to ensure Django is
configured before any test collection begins.

Per-app conftest.py files handle fixtures.

Docs: https://docs.pytest.org/en/stable/reference/fixtures.html#conftest-py-sharing-fixtures-across-files
"""
import django
from django.conf import settings


def pytest_configure():
    """Configure Django settings before test collection."""
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Imali.settings.production")
    django.setup()
