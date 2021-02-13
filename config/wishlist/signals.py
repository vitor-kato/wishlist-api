from customers.models import Customer
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Wishlist


@receiver(post_save, sender=Customer)
def create_customer_wishlist(sender, instance, created, **kwargs):
    if created:
        Wishlist.objects.create(customer=instance)
