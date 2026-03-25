"""
Selectors implementing all read operations and queryset composition.

Docs: https://docs.djangoproject.com/en/stable/topics/db/queries/

Rules:
    - Accept plain Python types — never request or view objects.
    - Return querysets or model instances — never serialized data or dicts.
    - Never perform any write operations.
    - Keep querysets lazy — let the caller decide when to evaluate them.
    - Input serializer queryset scoping (e.g. filtering by user) belongs here.
    - Raise NotFound from exceptions.py when a single object lookup fails.

Example:
    def get_post_by_slug(*, slug):
        try:
            return Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            raise NotFound(f"Post with slug '{slug}' not found.")

    def get_posts_for_user(*, user):
        if user.is_staff:
            return Post.objects.all()
        return Post.objects.filter(author=user)
"""

###
from decimal import Decimal
from django.db.models import Sum, Q
from apps_directory.transactions.managers import TransactionQuerySet
from apps_directory.transactions.models import Merchant, Transaction
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from accounts.models import CustomUser

class MerchantSelector:
    def __init__(self, user):
        self.user = user

    @staticmethod
    def for_user(user):
        """
               The only sanctioned way to query merchants in this codebase.
               Always returns global merchants combined with the user's own merchants.
               Never query Merchant.objects directly outside this selector.
        """
        return Merchant.user_objects.for_user(user)


class TransactionSelector:
    def __init__(self, user):
        self.user = user

    def filtered(self, *, merchant=None, category=None, month=None):
        q = Q()
        if merchant:
            q &= Q(merchant=merchant)
        if category:
            q &= Q(category=category)
        qs = self.for_user().filter(q)
        if month:
            qs = qs.for_month(month=month)
        return qs

    def for_user(self) -> TransactionQuerySet:
        return Transaction.objects.for_user(self.user)

    def for_month(self, *, month):
        return self.for_user().for_month(month=month)

    def paid_for_month(self, *, month):
        return self.for_month(month=month).paid()

    def unpaid_for_month(self, *, month):
        return self.for_month(month=month).unpaid()

    def income_for_user(self):
        return self.for_user().income()

    def income_for_month(self, *, month):
        return self.income_for_user().for_month(month=month)

    def expenses_for_user(self):
        return self.for_user().expenses()

    def expenses_for_month(self, *, month):
        return self.expenses_for_user().for_month(month=month)

    def transfers_for_user(self):
        return self.for_user().transfers()

    def transfers_for_month(self, *, month):
        return self.transfers_for_user().for_month(month=month)

    def for_category(self, *, category):
        return self.for_user().for_category(category=category)

    def for_category_for_month(self, *, month, category):
        return self.for_category(category=category).for_month(month=month)

    def for_account(self, *, account):
        return self.for_user().for_account(account=account)

    def for_account_for_month(self, *, month, account):
        return self.for_account(account=account).for_month(month=month)


class TransactionSummarySelector:
    def __init__(self, user):
        self.transactions = TransactionSelector(user=user)
        self.user = user

    def total_income_for_month(self, *, month):
        total_income = (
                self.transactions.income_for_month(month=month).aggregate(
                    total=Sum("amount")
                )["total"] or Decimal("0")
        )
        return total_income

    def total_expenses_for_month(self, *, month):
        total_expenses = (
                self.transactions.expenses_for_month(month=month).aggregate(
                    total=Sum("amount")
                )["total"] or Decimal("0")
        )
        return total_expenses

    def net_income_for_month(self, *, month):
        total_income = self.total_income_for_month(month=month)
        total_expenses = self.total_expenses_for_month(month=month)
        return total_income - total_expenses

    def total_expenditure_for_category(self, *, category):
        total_expenditure = (
            self.transactions.for_category(category=category).aggregate(
                total=Sum("amount")
            )["total"] or Decimal("0")
        )
        return total_expenditure

    def total_expenditure_for_category_for_month(self, *, month, category):
        total_expenditure = (
            self.transactions.for_category_for_month(month=month, category=category).aggregate(
                total=Sum("amount")
            )["total"] or Decimal("0")
        )
        return total_expenditure

    def get_user(self):
        return self.user


class UserPreferencesSelector:
    def __init__(self, user):
        self.user: CustomUser = user

    def preferred_currency(self):
        return self.user.preferences.preferred_currency
