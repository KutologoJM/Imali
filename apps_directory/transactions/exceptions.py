"""
Domain-level exceptions raised by services and selectors.

Docs: https://docs.djangoproject.com/en/stable/topics/class-based-views/generic-display/

Rules:
    - Services and selectors raise these — never Django or DRF exceptions directly.
    - Views are responsible for catching these and mapping them to HTTP responses.
    - Keep exceptions descriptive and scoped to this app's domain.
    - Inherit from a shared base (AppError) so callers can catch broadly if needed.

Example:
    # In a service:
    if not post.is_published:
        raise PermissionDenied("Only published posts can be shared.")

    # In a view:
    try:
        share_post(post=post)
    except PermissionDenied as e:
        return Response({"detail": str(e)}, status=403)

    class AppError(Exception): # Base for all domain exceptions — catch this to catch everything.
        pass

    class PermissionDenied(AppError):
        pass

    class NotFound(AppError):
        pass

    class ValidationError(AppError):
        pass
"""
