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
import uuid
from datetime import datetime
###
from decimal import Decimal
from django.db.models import Sum, Q, QuerySet
from apps_directory.transactions.managers import TransactionQuerySet
from apps_directory.transactions.models import Merchant, Transaction, Category, Account
from apps_directory.transactions.constants import TransactionStatus, TransactionType
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


class CategorySelector:
    def __init__(self, user):
        self.user = user

    def for_user(self):
        return Category.objects.filter(user=self.user)

    def for_month(self, *, month):
        return self.for_user().for_month(month=month)


class TransactionSelector:
    def __init__(self, user):
        self.user = user

    def filtered_search(self, *, account=None, category=None, due_date=None, date_paid=None, tx_status=None,
                        tx_type=None,
                        query=""):
        q = Q()
        if account:
            q &= Q(account__name=account)
        if category:
            q &= Q(category__name=category)
        if due_date:
            q &= Q(due_date__month=due_date)
        if date_paid:
            q &= Q(date_paid__month=date_paid)
        if tx_status:
            q &= Q(status=tx_status)
        if tx_type:
            q &= Q(category__type=tx_type)

        search = Q(merchant__name__icontains=query) | Q(category__name__icontains=query) | Q(
            description__icontains=query)
        try:
            uuid.UUID(query)
            search |= Q(uuid=query)
        except ValueError:
            pass

        try:
            month_number = datetime.strptime(query.capitalize(), "%B").month
            search |= Q(due_date__month=month_number) | Q(date_paid__month=month_number)
        except ValueError:
            pass

        filtered_queryset = Transaction.objects.for_user(user=self.user).filter(q)
        result = filtered_queryset.filter(search)
        return result

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

    def get_date_paid_months(self):
        return self.for_user().filter(date_paid__isnull=False).dates('date_paid', 'month')

    def get_due_date_months(self) -> QuerySet:
        return self.for_user().filter(due_date__isnull=False).dates('due_date', 'month')


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


class AccountsSelector:
    def __init__(self, user):
        self.user: CustomUser = user

    def for_user(self):
        return Account.objects.filter(user=self.user)


class TransactionMetadataSelector:
    @staticmethod
    def get_transaction_types():
        tx_types = TransactionType.choices
        return tx_types

    @staticmethod
    def get_transaction_statuses():
        tx_statuses = TransactionStatus.choices
        return tx_statuses
