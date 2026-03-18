"""
Tests for selector functions in selectors/__init__.py.

Docs: https://docs.pytest.org/en/stable/

Rules:
    - Test selectors in complete isolation — no views, no serializers, no HTTP.
    - Create objects via factories, call the selector, assert on the result.
    - Test both the happy path and edge cases (empty querysets, NotFound, etc.).
    - Never test ORM behaviour itself — test that the selector returns what is expected.

Example:
    @pytest.mark.django_db
    def test_get_post_by_slug_returns_correct_post():
        post = PostFactory(slug="hello-world")
        result = get_post_by_slug(slug="hello-world")
        assert result == post

    @pytest.mark.django_db
    def test_get_post_by_slug_raises_not_found_for_missing_slug():
        with pytest.raises(NotFound):
            get_post_by_slug(slug="does-not-exist")
"""
