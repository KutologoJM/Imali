"""
End-to-end tests for Django template views in views/web.py.

Docs: https://docs.djangoproject.com/en/stable/topics/testing/tools/

Rules:
    - Use Django's test Client — not DRF's APIClient.
    - Test status codes, redirects, template context, and form error rendering.
    - Do not re-test selector or service logic here — assume those layers are correct.
    - Use client.force_login() to authenticate without going through the login flow.

Example:
    @pytest.mark.django_db
    def test_post_list_redirects_unauthenticated_user(client):
        response = client.get(reverse("posts:list"))
        assert response.status_code == 302

    @pytest.mark.django_db
    def test_post_list_returns_200_for_authenticated_user(client, user):
        client.force_login(user)
        response = client.get(reverse("posts:list"))
        assert response.status_code == 200
"""
