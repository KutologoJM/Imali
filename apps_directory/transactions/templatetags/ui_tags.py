from typing import TYPE_CHECKING

from babel.numbers import format_currency
from django import template
from django.utils import timezone

if TYPE_CHECKING:
    from apps_directory.transactions.models import Transaction, Category
from apps_directory.transactions.selectors import UserPreferencesSelector, TransactionSummarySelector
register = template.Library()


@register.inclusion_tag("components/tx_table_field.html")
def tx_table_field(transaction: "Transaction"):
    category = transaction.category
    currency = transaction.account.currency
    formatted_amount = format_currency(
        number=transaction.amount,
        currency=currency.currency_code,
        locale=currency.locale,
    )
    return {
        "bg_color": category.bg_color,
        "icon_color": category.icon_color,
        "icon": category.icon,
        "merchant": transaction.merchant.name,
        "category": category.name,
        "amount": formatted_amount,
        "status": transaction.get_status_display().lower(),
        "date_paid": transaction.date_paid or "N/A",
        "due_date": transaction.due_date or "N/A",
    }

@register.inclusion_tag("components/monthly_balance_summary_card.html")
def monthly_balance_summary_card(transaction_summary_selector, month=None):
    user = transaction_summary_selector.get_user()
    currency = UserPreferencesSelector(user=user).preferred_currency()

    def _currency_formatter(value):
        return format_currency(
            value, currency=currency.currency_code, locale=currency.locale
        )

    total_expenses = transaction_summary_selector.total_expenses_for_month(month=month)
    total_income = transaction_summary_selector.total_income_for_month(month=month)
    net_income = transaction_summary_selector.net_income_for_month(month=month)
    net_income_status = "positive" if net_income >= 0 else "negative"

    if month is None:
        display_month = timezone.now().strftime("%B")
    else:
        display_month = month.strftime("%B")
    return {
        "total_expenses": _currency_formatter(total_expenses),
        "total_income": _currency_formatter(total_income),
        "net_income": _currency_formatter(net_income),
        "net_income_status": net_income_status,
        "month": display_month,
    }

@register.inclusion_tag("components/monthly_category_summary_card.html")
def monthly_category_summary_card(category: "Category", month=None):
    name = category.name
    user = category.user
    currency = UserPreferencesSelector(user=user).preferred_currency()
    amount = TransactionSummarySelector(user=user).total_expenditure_for_category_for_month(category=category, month=month)
    formatted_amount = format_currency(
        amount,
        currency=currency.currency_code,
        locale=currency.locale,
    )
    status = "info" # todo placeholder, required budgets app
    value = None # same as above
    return {
       "name": name,
        "amount": formatted_amount,
        "status": status,
        "value": value,
    }
