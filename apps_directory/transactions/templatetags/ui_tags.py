from typing import TYPE_CHECKING

from babel.numbers import format_currency
from django import template

if TYPE_CHECKING:
    from apps_directory.transactions.models import Transaction

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
