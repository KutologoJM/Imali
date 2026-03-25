"""
Services implementing all write operations: create, update, delete, and side effects.

Docs: https://docs.djangoproject.com/en/stable/topics/db/queries/

Rules:
    - Accept plain Python types or model instances — never request or view objects.
    - Raise domain exceptions from exceptions.py — never Django or DRF exceptions.
    - Call selectors for any reads required during a write operation.
    - Call external.py for any third-party side effects such as email or file storage.
    - Never return querysets — return model instances or primitives.
    - Use keyword-only arguments (*) to prevent positional argument mistakes.

Example:
    def create_post(*, user, title, body, tag_ids=None):
        if Post.objects.filter(title=title).exists():
            raise ValidationError("A post with this title already exists.")
        post = Post.objects.create(author=user, title=title, body=body)
        if tag_ids:
            post.tags.set(tag_ids)
        return post
"""
