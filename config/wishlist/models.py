from customers.models import Customer
from django.db import models

from config.base_models import BaseAbstractModel

from .client import ProductClient


class Wishlist(BaseAbstractModel):
    customer = models.OneToOneField(
        Customer, related_name="wishlist", on_delete=models.CASCADE, blank=False
    )


class Product(BaseAbstractModel):
    external_id = models.CharField(max_length=300, blank=False)
    wishlist = models.ManyToManyField(
        Wishlist,
        related_name="products",
        blank=True,
    )

    def save(self, *args, **kwargs):
        c = ProductClient(self.external_id)
        c.get_data()
        super(Product, self).save(*args, **kwargs)

    def get_product_data(self):
        c = ProductClient(self.external_id)
        product_data = c.get_cache()
        return product_data
