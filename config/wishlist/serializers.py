from django.core.paginator import Paginator
from rest_framework import serializers, pagination
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.reverse import reverse

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
    next = serializers.SerializerMethodField()
    previous = serializers.SerializerMethodField()

    class Meta:
        model = Wishlist
        # fields = "__all__"
        exclude = ("id", "created_at", "updated_at", "customer")

    def get_total_products(self, instance):
        self.total = instance.products.count()
        return self.total

    def set_next_previous_url(self, instance, page_number):
        query_param = "product_page"
        params = f"?{query_param}={page_number}"
        params += f"&size={self.page_size}"

        r = reverse(
            "customer-detail",
            args=[instance.pk],
            request=self.context.get("request"),
        )
        return r + params

    def get_next(self, instance):
        if getattr(self, "next", None):
            r = self.set_next_previous_url(instance, self.next)
            return r

    def get_previous(self, instance):
        if getattr(self, "previous", None):
            r = self.set_next_previous_url(instance, self.previous)
            return r

    def get_pagination(self, instance):
        page_size = int(api_settings.PAGE_SIZE)
        page_number = 1
        if self.context:
            page_size = (
                self.context.get("request").query_params.get("size") or page_size
            )
            page_number = (
                self.context.get("request").query_params.get("product_page")
                or page_number
            )
        paginator = Paginator(instance.products.all(), page_size)
        page = paginator.page(page_number)

        self.page_size = page_size
        if self.context.get("request"):
            if page.has_next():
                self.next = page.next_page_number()
            if page.has_previous():
                self.previous = page.previous_page_number()

        return page

    def paginated_products(self, instance):
        products = self.get_pagination(instance)
        serializer = ProductSerializer(products, many=True)
        return serializer.data
