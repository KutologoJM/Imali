"""
Registers models with the Django admin site.

Docs: https://docs.djangoproject.com/en/stable/ref/contrib/admin/

Rules:
    - Register every model that needs to be managed via the admin interface.
    - Use ModelAdmin subclasses to customize list views, search, and filters.
    - Never put business logic here — admin actions should call services.

Example:
    @admin.register(Post)
    class PostAdmin(admin.ModelAdmin):
        list_display = ["title", "author", "is_published", "created_at"]
        list_filter = ["is_published"]
        search_fields = ["title", "author__username"]
"""
