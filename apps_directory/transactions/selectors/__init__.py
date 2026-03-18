"""
Selectors implementing all read operations and queryset composition.

Docs: https://docs.djangoproject.com/en/stable/topics/db/queries/

Rules:
    - Accept plain Python types — never request or view objects.
    - Return querysets or model instances — never serialized data or dicts.
    - Never perform any write operations.
    - Keep querysets lazy — let the caller decide when to evaluate them.
    - Input serializer queryset scoping (e.g. filtering by user) belongs here.
    - Raise NotFound from exceptions.py when a single object lookup fails.

Example:
    def get_post_by_slug(*, slug):
        try:
            return Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            raise NotFound(f"Post with slug '{slug}' not found.")

    def get_posts_for_user(*, user):
        if user.is_staff:
            return Post.objects.all()
        return Post.objects.filter(author=user)
"""
from apps_directory.transactions.models import Merchant


def get_merchants_for_user(*, user):
    """
    The only sanctioned way to query merchants in this codebase.
    Always returns global merchants combined with the user's own merchants.
    Never query Merchant.objects directly outside of this selector.
    """
    return Merchant.objects.for_user(user)