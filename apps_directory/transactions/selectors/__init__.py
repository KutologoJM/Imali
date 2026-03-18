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
from decimal import Decimal

from django.db.models import Sum

from apps_directory.transactions.models import Merchant, Transaction
from django.db import models


def get_merchants_for_user(*, user):
    """
    The only sanctioned way to query merchants in this codebase.
    Always returns global merchants combined with the user's own merchants.
    Never query Merchant.objects directly outside of this selector.
    """
    return Merchant.objects.for_user(user)


# Unpaid
def get_user_unpaid_transactions_for_month(*, month, user):
    return get_all_user_transactions_for_month(user=user, month=month).unpaid()


# Paid
def get_user_paid_transactions_for_month(*, month, user):
    return get_all_user_transactions_for_month(user=user, month=month).paid()


# Net Balance
def get_user_net_balance_for_month(*, user, month):
    total_income = (
        get_user_total_income_for_month(user=user, month=month)
        .aggregate(total=Sum("amount"))["total"] or Decimal("0")
    )
    total_expenses = (
        get_users_total_expenses_for_month(user=user, month=month)
        .aggregate(total=Sum("amount"))["total"] or Decimal("0")
    )
    return total_income - total_expenses


# All - no filter
def get_all_user_transactions(*, user):
    return Transaction.objects.for_user(user)


# Time
def get_all_user_transactions_for_month(*, user, month):
    return get_all_user_transactions(user=user).for_month(month=month)


# Income
def get_all_user_income_transactions(*, user):
    return get_all_user_transactions(user=user).income()


def get_user_total_income_for_month(*, user, month):
    return get_all_user_income_transactions(user=user).for_month(month=month)


# Expenses
def get_all_user_expenses(*, user):
    return get_all_user_transactions(user=user).expenses()


def get_users_total_expenses_for_month(*, user, month):
    return get_all_user_expenses(user=user).for_month(month=month)


# Transfers
def get_all_user_transfers(*, user):
    return get_all_user_transactions(user=user).transfers()


def get_all_user_transfers_for_month(*, user, month):
    return get_all_user_transfers(user=user).for_month(month=month)


# Category
def get_user_monthly_transactions_by_category(*, category, user, month):
    return get_all_user_transactions_for_month(user=user, month=month).for_category(category)


# Search bar
def get_filtered_user_transactions(*, user, merchant=None, category=None, month=None):
    q = models.Q()

    if merchant:
        q &= models.Q(merchant=merchant)
    if category:
        q &= models.Q(category=category)

    transactions = Transaction.objects.for_user(user).filter(q)

    if month:
        transactions = transactions.for_month(month=month)

    return transactions


# Account
def get_all_user_transactions_for_account(*, user, account):
    return get_all_user_transactions(user=user).for_account(account=account)


def get_all_user_transactions_for_account_for_month(*, user, month, account):
    return get_all_user_transactions_for_account(user=user, account=account).for_month(month=month)
