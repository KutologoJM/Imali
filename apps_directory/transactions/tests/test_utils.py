"""
Tests for utility functions in utils/__init__.py.

Docs: https://docs.pytest.org/en/stable/

Rules:
    - Utility tests need no DB access — omit the db fixture entirely.
    - Test every branch of conditional logic.
    - Keep tests short: one assertion per test is ideal for pure functions.
    - No mocking should be needed — if it is, the function may not be a true utility.

Example:
    def test_truncate_short_string_unchanged():
        assert truncate("Hello", max_length=10) == "Hello"

    def test_truncate_long_string_adds_suffix():
        result = truncate("Hello World", max_length=8, suffix="...")
        assert result == "Hello..."
        assert len(result) == 8
"""
