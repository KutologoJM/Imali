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
from django.urls import path
from apps_directory.transactions.views import web as web_views

app_name = "transactions"
urlpatterns = [
    path("", web_views.index, name="index"),
    path("monthly-category-summary/", web_views.monthly_category_summary, name="monthly_category_summary"),
    path("monthly-balance-summary/", web_views.monthly_balance_summary, name="monthly_balance_summary"),
    path("transactions-table/", web_views.transactions_table, name="transactions_table"),
    path("search-and-filter/", web_views.search_and_filter_transactions, name="search_and_filter_transactions"),
    path('create/<slug:form_slug>/', web_views.universal_create_view, name='universal_create'),

]
