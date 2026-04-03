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
from django import forms
from django.http import HttpResponseNotFound
from django.shortcuts import render
from apps_directory.transactions.selectors import TransactionSelector, TransactionSummarySelector, CategorySelector, \
    AccountsSelector, TransactionMetadataSelector
from apps_directory.transactions.forms.web import AccountForm, MerchantForm, CategoryForm


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
    if request.method == "GET":  # runs once during the initial load
        context["transactions"] = TransactionSelector(user=request.user).for_user().select_related(
            "category",
            "merchant",
            "account__currency")
    elif request.method == "POST":
        query = request.POST.get("transaction_query")
        account = request.POST.get("account")
        due_date = request.POST.get("due_date")
        date_paid = request.POST.get("date_paid")
        transaction_status = request.POST.get("tx_status")
        transaction_type = request.POST.get("tx_type")
        transactions = TransactionSelector(user=request.user).filtered_search(query=query, account=account,
                                                                              due_date=due_date, date_paid=date_paid,
                                                                              tx_status=transaction_status,
                                                                              tx_type=transaction_type)
        context["transactions"] = transactions.select_related(
            "category",
            "merchant",
            "account__currency")
    else:
        return HttpResponseNotFound("404")
    return render(request, 'partials/transactions_table.html', context)


def search_and_filter_transactions(request):
    context = {}
    if request.method == "GET":  # Loads the initial filter options for the given user
        context["accounts"] = AccountsSelector(user=request.user).for_user().select_related()
        context["dates_paid"] = TransactionSelector(user=request.user).get_date_paid_months()
        context["due_dates"] = TransactionSelector(user=request.user).get_due_date_months()
        context["transaction_statuses"] = TransactionMetadataSelector.get_transaction_statuses()
        context["transaction_types"] = TransactionMetadataSelector.get_transaction_types()
        return render(request, "partials/search_and_filter_form.html", context)
    else:
        return HttpResponseNotFound("404")


def universal_create_view(request, form_slug):
    context = {}
    form_mapping = {
        "merchant-form": MerchantForm,
        "category-form": CategoryForm,
        "account-form": AccountForm,
    }
    form_name = str(form_slug).split('-')[0]
    context['form_name'] = form_name

    if request.method == "GET":
        context["form_slug"] = form_slug
        context["form"] = form_mapping[form_slug]
        return render(request, 'components/universal_form_card.html', context)
    elif request.method == "POST":
        match form_slug:
            case "merchant-form":
                form = MerchantForm(request.POST)
                needs_user = True
            case "category-form":
                form = CategoryForm(request.POST)
                needs_user = True
            case "account-form":
                form = AccountForm(request.POST)
                needs_user = True
            case _:
                return HttpResponseNotFound("404")

        if form.is_valid(): # fixme merchant validation broken
            form_instance = form.save(commit=False)
            if needs_user:
                form_instance.user = request.user
            form_instance.save()
            return render(request, 'components/feedback/form_creation_success.html', context)
        else:
            context["form_slug"] = form_slug
            context["form"] = form
            context['status'] = 400
            return render(request, 'components/universal_form_card.html', context)
    else:
        return HttpResponseNotFound("404")
