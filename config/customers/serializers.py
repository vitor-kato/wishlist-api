from rest_framework import serializers

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for customer data """

    class Meta:
        model = Customer
        exclude = ("user",)
