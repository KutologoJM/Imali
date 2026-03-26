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
from django.shortcuts import render

from apps_directory.transactions.models import Category
from apps_directory.transactions.selectors import TransactionSelector, TransactionSummarySelector


def dashboard(request):
    context = {}

    context["transactions"] = TransactionSelector(user=request.user).for_user().select_related("category", "merchant",
                                                                                               "account__currency")
    context["transaction_summary_selector"] = TransactionSummarySelector(user=request.user)
    context["categories"] = Category.objects.filter(user=request.user)
    return render(request, 'pages/Dashboard.html', context)


def index(request):
    """
      This view will serve as the main page for the transactions app.
    """
    context = {}

    return render(request, 'pages/index.html', context)