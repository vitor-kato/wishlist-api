from customers.models import Customer
from django.db import models

from config.base_models import BaseAbstractModel


class Wishlist(BaseAbstractModel):
    customer = models.OneToOneField(
        Customer, related_name="wishlist", on_delete=models.CASCADE, blank=False
    )


class Product(BaseAbstractModel):
    external_id = models.CharField(max_length=300, blank=False)
    wishlist = models.ForeignKey(
        Wishlist,
        on_delete=models.SET_NULL,
        related_name="products",
        blank=False,
        null=True,
    )
