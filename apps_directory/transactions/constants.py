"""
App-wide constants, enumerations, and Django field choices.

Docs: https://docs.djangoproject.com/en/stable/ref/models/fields/#choices

Rules:
    - Use TextChoices or IntegerChoices instead of plain tuples or string literals.
    - Import from here rather than redefining values in models or serializers.
    - Keep constants grouped by the concept they represent.
    - Never import models here — this file must be importable with no side effects.

Example:
    from django.db import models

    class PostStatus(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"
"""
from django.db import models

class TransactionType(models.TextChoices):
    EXPENSE = "expense", "Expense"
    INCOME = "income", "Income"
    TRANSFER = "transfer", "Transfer"

class TransactionStatus(models.TextChoices):
    UNPAID = "unpaid", "Unpaid" # default state, user or system
    PAID = "paid", "Paid" # user decided
    MISSED = "missed", "Missed" # system, missed payment due on this date
    CANCELLED = "cancelled", "Cancelled" # user designated, planned payment but cancelled