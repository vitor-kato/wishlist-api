from rest_framework import serializers

from .models import Product, Wishlist


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product data """

    class Meta:
        model = Product
        fields = "__all__"


class WishlistSerializer(serializers.ModelSerializer):
    """Serializer for Wishlist data """

    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Wishlist
        fields = "__all__"
