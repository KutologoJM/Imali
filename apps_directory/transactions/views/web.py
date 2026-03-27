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
from django.http import HttpResponseNotFound
from django.shortcuts import render
from apps_directory.transactions.selectors import TransactionSelector, TransactionSummarySelector, CategorySelector


def index(request):
    """
      This view will serve as the main page for the transactions app.
    """
    context = {}

    return render(request, 'pages/index.html', context)


def monthly_category_summary(request):
    context = {}
    if request.method == "GET":
        context["categories"] = CategorySelector(user=request.user).for_user().select_related("user__preferences", )
        return render(request, "partials/monthly_category_summary.html", context)
    elif request.method == "POST":
        month = request.POST.get("month")
        context["categories"] = CategorySelector(user=request.user).for_month(month=month).select_related(
            "user__preferences", )
        return render(request, "partials/monthly_category_summary.html", context)
    else:
        return HttpResponseNotFound("404")


def monthly_balance_summary(request):
    context = {}
    if request.method == "GET":
        context["transaction_summary_selector"] = TransactionSummarySelector(user=request.user)
        return render(request, 'partials/monthly_balance_summary.html', context)
    return HttpResponseNotFound("404")


def transactions_table(request):
    context = {}
    if request.method == "GET":
        context["transactions"] = TransactionSelector(user=request.user).for_user().select_related(
            "category",
            "merchant",
            "account__currency")
        return render(request, "partials/transactions_table.html", context)
    elif request.method == "POST":
        query = request.POST.get("transaction_query")
        context["transactions"] = TransactionSelector(user=request.user).filtered_search(query=query).select_related(
            "category",
            "merchant",
            "account__currency")
        return render(request, 'partials/transactions_table.html', context)
    else:
        return HttpResponseNotFound("404")
