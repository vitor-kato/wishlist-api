from django.core.paginator import Paginator
from rest_framework import serializers
from rest_framework.settings import api_settings

from .models import Product, Wishlist


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product data """

    data = serializers.SerializerMethodField()

    class Meta:
        model = Product
        # fields = "__all__"
        exclude = ("id", "wishlist", "created_at", "updated_at")

    def get_data(self, instance):
        return instance.get_product_data()

    def to_representation(self, obj):
        repr = super(ProductSerializer, self).to_representation(obj)
        repr.pop("external_id")
        return repr


class WishlistSerializer(serializers.ModelSerializer):
    """Serializer for Wishlist data """

    total_products = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField("paginated_products")

    class Meta:
        model = Wishlist
        # fields = "__all__"
        exclude = ("id", "created_at", "updated_at", "customer")

    def get_total_products(self, instance):
        return instance.products.count()

    def paginated_products(self, instance):
        page_size = api_settings.PAGE_SIZE
        page_number = 1
        if self.context:
            page_size = (
                self.context.get("request").query_params.get("size") or page_size
            )
            page_number = (
                self.context.get("request").query_params.get("page") or page_number
            )

        paginator = Paginator(instance.products.all(), page_size)
        products = paginator.page(page_number)
        serializer = ProductSerializer(products, many=True)
        return serializer.data
