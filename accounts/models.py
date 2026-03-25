from django.contrib.auth.models import AbstractUser
from django.db import models

from apps_directory.transactions.models import Currency


# Create your models here.

class CustomUser(AbstractUser):
    pass

class UserPreferences(models.Model):
    user = models.OneToOneField(
        "CustomUser",
        on_delete=models.CASCADE,
        related_name="preferences",
    )
    preferred_currency = models.ForeignKey("transactions.Currency", on_delete=models.PROTECT, related_name="preferred_by")
    class Meta:
        verbose_name_plural = "User preferences"

    def __str__(self):
        return f"{self.user.username} preferences"
