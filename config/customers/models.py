from django.db import models

from config.base_models import BaseAbstractModel, User


class Customer(BaseAbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customers")
    name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(max_length=255, blank=False, unique=True)
