"""
Wrappers for third-party service calls: email, SMS, file storage, payment providers, etc.

Docs: https://docs.djangoproject.com/en/stable/topics/email/

Rules:
    - All network-dependent side effects live here so they can be mocked cleanly in tests.
    - Called exclusively from services/__init__.py — never directly from views or tasks.
    - Functions here should do one thing: make the external call and raise on failure.
    - Never contain business logic — that belongs in services/__init__.py.

Example:
    def send_post_published_email(*, post):
        send_mail(
            subject=f"Your post '{post.title}' is now live.",
            message=f"View it at: /posts/{post.slug}/",
            from_email="noreply@example.com",
            recipient_list=[post.author.email],
        )
"""
