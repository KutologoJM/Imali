"""
Django view-level permission mixins for template views.

Docs: https://docs.djangoproject.com/en/stable/topics/auth/default/#the-permission-required-decorator

Rules:
    - Use Django's built-ins first: LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin.
    - Custom mixins go here only when built-ins are insufficient.
    - Mixins control view access — they are not a substitute for service-level permission checks.
    - Never put DRF permission classes in this file.

Example:
    class OwnerRequiredMixin(UserPassesTestMixin):
        owner_field = "owner"

        def test_func(self):
            obj = self.get_object()
            return getattr(obj, self.owner_field) == self.request.user
"""
