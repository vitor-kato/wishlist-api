from rest_framework import serializers
from wishlist.serializers import WishlistSerializer

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for customer data """

    wishlist = WishlistSerializer(read_only=True)

    class Meta:
        model = Customer
        exclude = ("user",)
