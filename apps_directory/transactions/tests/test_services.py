"""
Tests for service functions in services/__init__.py.

Docs: https://docs.pytest.org/en/stable/

Rules:
    - Test services in isolation — no views, no HTTP requests.
    - Mock all external.py calls using unittest.mock.patch to avoid network calls.
    - Test the happy path, domain exceptions, and observable side effects.
    - Assert on the returned object and on DB state, not on internal implementation.

Example:
    @pytest.mark.django_db
    def test_create_post_persists_to_db():
        user = UserFactory()
        post = create_post(user=user, title="Hello", body="World")
        assert Post.objects.filter(pk=post.pk).exists()

    @pytest.mark.django_db
    @patch("posts.services.external.send_post_published_email")
    def test_publish_post_sends_email(mock_email):
        post = PostFactory(status=PostStatus.DRAFT)
        publish_post(post=post)
        mock_email.assert_called_once_with(post=post)
"""
