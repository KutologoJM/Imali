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


class MerchantQuerySet(models.QuerySet):
    def for_user(self, user) -> Self:
        return self.filter(
            models.Q(is_global=True) | models.Q(user=user)
        )


class MerchantManager(models.Manager):
    def get_queryset(self) -> MerchantQuerySet:
        return MerchantQuerySet(self.model, using=self._db)

    def for_user(self, user) -> MerchantQuerySet:
        return self.get_queryset().for_user(user)