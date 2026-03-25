"""
Shared pytest fixtures for this app's test suite.

Docs: https://docs.pytest.org/en/stable/reference/fixtures.html

Rules:
    - Define fixtures used by more than one test file here.
    - Use factory fixtures (UserFactory, etc.) rather than creating objects inline.
    - Scope fixtures appropriately: function (default), class, module, or session.
    - For API tests, provide both an unauthenticated client and an authenticated one.

Example:
    @pytest.fixture
    def user(db):
        return UserFactory()

    @pytest.fixture
    def authenticated_client(user):
        client = APIClient()
        client.force_authenticate(user=user)
        return client, user
"""
