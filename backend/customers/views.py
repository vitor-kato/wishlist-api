from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from wishlist.models import Product
from wishlist.serializers import ProductSerializer

from .models import Customer
from .serializers import CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "email", "wishlist__products__external_id"]

    def validate_product(self):
        id = self.request.data.get("external_id")
        product_serializer = ProductSerializer(data={"external_id": id})
        return product_serializer, id

    # def get_queryset(self):
    #     return Customer.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"], url_path="add-product")
    def add_product(self, request, pk=None):
        customer = self.get_object()
        wishlist = customer.wishlist

        product_serializer, id = self.validate_product()
        if not product_serializer.is_valid():
            return Response(product_serializer.errors)

        product, _ = Product.objects.get_or_create(external_id=id)
        product.wishlist.add(wishlist)

        return Response(
            CustomerSerializer(customer).data, status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["post"], url_path="remove-product")
    def remove_product(self, request, pk=None):
        customer = self.get_object()
        wishlist = customer.wishlist

        product_serializer, id = self.validate_product()
        if not product_serializer.is_valid():
            return Response(product_serializer.errors)

        product = Product.objects.get(external_id=id)
        product.wishlist.remove(wishlist)

        return Response(CustomerSerializer(customer).data, status=status.HTTP_200_OK)
