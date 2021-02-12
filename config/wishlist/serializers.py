from rest_framework import serializers

from .models import Product, Wishlist


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product data """

    data = serializers.SerializerMethodField()

    class Meta:
        model = Product
        # fields = "__all__"
        exclude = ("id", "external_id", "wishlist", "created_at", "updated_at")

    def get_data(self, instance):
        return instance.get_product_data()


class WishlistSerializer(serializers.ModelSerializer):
    """Serializer for Wishlist data """

    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Wishlist
        # fields = "__all__"
        exclude = ("created_at", "updated_at")
