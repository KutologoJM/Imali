"""
Stateless utility functions with no database access and no side effects.

Docs: https://docs.python.org/3/library/functions.html

Rules:
    - Functions here must be pure: same input always produces the same output.
    - No database access — if a helper needs the DB, it belongs in selectors.
    - No side effects — if a helper sends email or writes files, it belongs in external.py.
    - Utilities should be generic enough to be used across multiple apps.

Example:
    def build_full_name(first_name, last_name):
        return f"{first_name} {last_name}".strip()

    def truncate(text, max_length=100, suffix="..."):
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix
"""
