"""
URL routing for Django template-rendered views.

Docs: https://docs.djangoproject.com/en/stable/topics/http/urls/

Rules:
    - Mount these under a logical prefix in the root urls.py using include().
    - Use an app_name for namespacing so url template tags and reverse() calls are unambiguous.
    - Use <slug:slug> or <int:pk> converters — avoid unconstrained <str:> captures.
    - Keep URL patterns readable; one view per path, no inline logic.

Example:
    # root urls.py
    path("posts/", include(("posts.urls.web", "posts"), namespace="posts")),

    # this file
    urlpatterns = [
        path("", PostListView.as_view(), name="list"),
        path("create/", PostCreateView.as_view(), name="create"),
        path("<slug:slug>/", PostDetailView.as_view(), name="detail"),
    ]
"""
