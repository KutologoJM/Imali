"""
Django ORM model definitions for this app.

Docs: https://docs.djangoproject.com/en/stable/topics/db/models/

Rules:
    - Models are pure data definitions — field declarations, Meta, and __str__ only.
    - Attach custom managers from managers.py for reusable queryset building blocks.
    - No business logic in models — that belongs in services.
    - No query composition in models — that belongs in selectors.
    - Use explicit field names and avoid relying on Django defaults for null/blank.

Example:
    class Post(models.Model):
        title = models.CharField(max_length=200)
        body = models.TextField()
        author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
        status = models.CharField(max_length=20, choices=PostStatus.choices, default=PostStatus.DRAFT)
        created_at = models.DateTimeField(auto_now_add=True)

        objects = models.Manager()
        published = PublishedManager()

        class Meta:
            ordering = ["-created_at"]

        def __str__(self):
            return self.title
"""

from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models

from apps_directory.transactions.constants import TransactionType, TransactionStatus
from apps_directory.transactions.managers import MerchantManager, TransactionQuerySet
from core.models import TimeStampedModel
from django.core.exceptions import ValidationError

User = get_user_model()


class Account(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")
    name = models.CharField(max_length=100)
    group = models.ForeignKey(
        "AccountGroup", on_delete=models.PROTECT)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.ForeignKey(
        "Currency", on_delete=models.PROTECT, related_name="accounts"
    )
    provider = models.CharField(max_length=100)

    objects = models.Manager()

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Accounts"

    def __str__(self):
        return f"{self.provider} {self.group.name} Account ({self.currency.currency_code})"


class AccountGroup(TimeStampedModel):
    name = models.CharField(max_length=50, unique=True,
                            help_text="Supported account groups. E.g. Savings, Credit Card, Cash")
    description = models.TextField(default="No description")

    objects = models.Manager()

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Account Groups"

    def __str__(self):
        return f"{self.name}"


class Currency(TimeStampedModel):
    name = models.CharField(max_length=50)
    currency_code = models.CharField(max_length=3, unique=True)
    currency_symbol = models.CharField(max_length=5)
    locale = models.CharField(max_length=20)

    objects = models.Manager()

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Currencies"

    def __str__(self):
        return f"({self.currency_code}) {self.currency_symbol} {self.name}"


class Merchant(TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="merchants", null=True, blank=True)
    name = models.CharField(max_length=100, help_text="E.g. Netflix, Youtube, Landlord")
    description = models.TextField(default="No description")
    is_global = models.BooleanField(default=False)

    objects = models.Manager()  # default — for Django internals and admin
    user_objects = MerchantManager()  # for all application code

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Merchants"

    def __str__(self):
        return f"{self.name}"

    def clean(self):
        super().clean()
        if self.is_global and self.user is not None:
            raise ValidationError({
                "user": "A global merchant must not be assigned to a user"
            })

    def save(self, *args, **kwargs):
        if self.is_global and self.user is not None:
            raise ValueError(
                "A global merchant must not be assigned to a user"
            )
        super().save(*args, **kwargs)


class Category(TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="categories",
    )
    name = models.CharField(max_length=50, help_text="E.g. Utilities, Groceries")
    description = models.TextField(default="No description")
    type = models.CharField(choices=TransactionType, default=TransactionType.EXPENSE, max_length=50)
    icon = models.CharField(max_length=100)  # font-awesome icon
    icon_color = models.CharField(max_length=30)  # "#ffb400"
    bg_color = models.CharField(max_length=40)  # "rgba(255,180,0,0.12)"

    objects = models.Manager()

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name} ({self.type})"

    @property
    def icon_url(self):
        return f"/static/icons/{self.icon}"


class Transaction(TimeStampedModel):
    uuid = models.UUIDField(unique=True, default=uuid4)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="transactions",
    )
    account = models.ForeignKey(
        "Account", on_delete=models.PROTECT, related_name="transactions"
    )
    destination_account = models.ForeignKey(
        "Account", on_delete=models.PROTECT, related_name="incoming_transactions", null=True, blank=True,
        help_text="Recipient account used for transfers"
    )
    merchant = models.ForeignKey(
        "Merchant", on_delete=models.PROTECT, related_name="transactions"
    )
    category = models.ForeignKey(
        "Category", on_delete=models.PROTECT, related_name="transactions"
    )
    """associated_bill = models.ForeignKey(
        "RecurringBill", on_delete=models.SET_NULL, related_name="transactions", null=True,
    )"""
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(choices=TransactionStatus, default=TransactionStatus.UNPAID, max_length=50)
    due_date = models.DateField(null=True, blank=True)
    date_paid = models.DateField(null=True, blank=True)
    description = models.TextField(default="No description")
    notes = models.TextField(default="No notes")

    objects = TransactionQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Transactions"

    def __str__(self):
        currency_symbol = self.account.currency.currency_symbol

        if not self.date_paid:
            return f"{self.status.capitalize()} transaction: {currency_symbol}{self.amount} to {self.merchant}."

        if self.category.type == TransactionType.EXPENSE:
            return f"Paid {currency_symbol}{self.amount} to {self.merchant} on {self.date_paid}."
        elif self.category.type == TransactionType.INCOME:
            return f"Received {currency_symbol}{self.amount} from {self.merchant} on {self.date_paid}."
        elif self.category.type == TransactionType.TRANSFER:
            return f"Transferred {currency_symbol}{self.amount} to {self.destination_account} on {self.date_paid}."
        else:
            return f"Invalid transaction: {currency_symbol}{self.amount} on {self.date_paid}."

    def clean(self):
        super().clean()

        if self.status == TransactionStatus.UNPAID:
            if not self.due_date:
                raise ValidationError({
                    "due_date": "Unpaid transactions must have a due date"
                })
            if self.date_paid:
                raise ValidationError({
                    "date_paid": "Unpaid transactions cannot have a payment date"
                })

        if self.status == TransactionStatus.PAID:
            if not self.date_paid:
                raise ValidationError({
                    "date_paid": "A corresponding payment date is required"
                })

        if self.status == TransactionStatus.MISSED:
            if not self.due_date:
                raise ValidationError({
                    "due_date": "Missed transactions must have a due date"
                })
            if self.date_paid:
                raise ValidationError({
                    "date_paid": "Missed transactions cannot have a payment date"
                })

        if self.status == TransactionStatus.CANCELLED:
            if self.date_paid:
                raise ValidationError({
                    "date_paid": "Cancelled transactions cannot have a payment date"
                })

    def save(self, *args, **kwargs):
        if self.status == TransactionStatus.UNPAID:
            if not self.due_date:
                raise ValueError("Unpaid transactions must have a due date")
            if self.date_paid:
                raise ValueError("Unpaid transactions cannot have a payment date")

        if self.status == TransactionStatus.PAID:
            if not self.date_paid:
                raise ValueError("A corresponding payment date is required")

        if self.status == TransactionStatus.MISSED:
            if not self.due_date:
                raise ValueError("Missed transactions must have a due date")
            if self.date_paid:
                raise ValueError("Missed transactions cannot have a payment date")

        if self.status == TransactionStatus.CANCELLED:
            if self.date_paid:
                raise ValueError("Cancelled transactions cannot have a payment date")

        super().save(*args, **kwargs)
