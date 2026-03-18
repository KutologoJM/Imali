"""
Custom model managers providing reusable queryset building blocks.

Docs: https://docs.djangoproject.com/en/stable/topics/db/managers/

Rules:
    - Managers provide generic, reusable ORM primitives — not business logic.
    - Business logic belongs in services; query composition belongs in selectors.
    - Override get_queryset() for default filtering (e.g. soft-delete patterns).
    - Use Manager over QuerySet subclass when the method must be on the manager itself.

Example:
    class PublishedManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status=PostStatus.PUBLISHED)

    class Post(models.Model):
        objects = models.Manager()       # default, unrestricted
        published = PublishedManager()   # scoped
"""
from typing import Self
from django.db import models
from django.utils import timezone
from apps_directory.transactions.constants import TransactionType, TransactionStatus


class MerchantQuerySet(models.QuerySet):

    def for_user(self, user) -> Self:
        return self.filter(
            models.Q(is_global=True) | models.Q(user=user)
        )


class MerchantManager(models.Manager):
    def get_queryset(self):
        raise NotImplementedError(
            "MerchantManager requires a user. Use Merchant.objects.for_user(user) instead."
        )

    def for_user(self, user) -> MerchantQuerySet:
        return MerchantQuerySet(self.model, using=self._db).for_user(user)


class TransactionQuerySet(models.QuerySet):

    def for_user(self, user) -> Self:
        return self.filter(user=user)

    def for_month(self, *, year=None, month=None) -> Self:
        now = timezone.now()
        return self.filter(
            date_paid__year=year or now.year,
            date_paid__month=month or now.month,
        )

    def unpaid(self) -> Self:
        return self.filter(status=TransactionStatus.UNPAID)

    def paid(self) -> Self:
        return self.filter(status=TransactionStatus.PAID)

    def income(self) -> Self:
        return self.filter(category__type=TransactionType.INCOME)

    def expenses(self) -> Self:
        return self.filter(category__type=TransactionType.EXPENSE)

    def transfers(self) -> Self:
        return self.filter(category__type=TransactionType.TRANSFER)

    def for_account(self, account) -> Self:
        return self.filter(account=account)

    def in_date_range(self, start, end) -> Self:
        return self.filter(date_paid__range=(start, end))

    def for_category(self, category) -> Self:
        return self.filter(category=category)

    def for_merchant(self, merchant) -> Self:
        return self.filter(merchant=merchant)