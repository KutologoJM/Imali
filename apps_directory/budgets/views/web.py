"""
Django class-based views rendering HTML templates.

Docs: https://docs.djangoproject.com/en/stable/topics/class-based-views/

Rules:
    - Views are thin coordinators — no business logic, no raw ORM queries.
    - Call selectors for reads, services for writes.
    - Catch domain exceptions from exceptions.py and map them to redirects or form errors.
    - Never pass request objects into services or selectors.
    - Extract form.cleaned_data and pass to a service — never call form.save().

Example:
    class PostCreateView(LoginRequiredMixin, CreateView):
        template_name = "posts/create.html"
        form_class = PostForm

        def form_valid(self, form):
            try:
                create_post(user=self.request.user, **form.cleaned_data)
                return redirect("posts:list")
            except ValidationError as e:
                form.add_error(None, str(e))
                return self.form_invalid(form)
"""
