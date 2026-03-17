from django.contrib.auth.models import User
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserOwnedModel(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True
