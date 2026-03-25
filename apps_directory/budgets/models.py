"""
Django ORM model definitions for this app.

Docs: https://docs.djangoproject.com/en/stable/topics/db/models/

Rules:
    - Models are pure data definitions — field declarations, Meta, and __str__ only.
    - Attach custom managers from managers.py for reusable queryset building blocks.
    - No business logic in models — that belongs in services.
    - No query composition in models — that belongs in selectors.
    - Use explicit field names and avoid relying on Django defaults for null/blank.

Example:
    class Post(models.Model):
        title = models.CharField(max_length=200)
        body = models.TextField()
        author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
        status = models.CharField(max_length=20, choices=PostStatus.choices, default=PostStatus.DRAFT)
        created_at = models.DateTimeField(auto_now_add=True)

        objects = models.Manager()
        published = PublishedManager()

        class Meta:
            ordering = ["-created_at"]

        def __str__(self):
            return self.title
"""
