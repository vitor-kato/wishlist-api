import unittest

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from config.base_models import User

from .models import Customer
from .views import CustomerViewSet


class CustomerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test-user", password="")
        Customer.objects.create(user=self.user, name="test-name", email="test-email")

    @unittest.expectedFailure
    def test_duplicate_email(self):
        Customer.objects.create(user=self.user, name="test-name", email="test-email")


class CustomerViewsTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username="test-user", password="")
        self.external_id = "1bf0f365-fbdd-4e21-9786-da459d78dd1f"
        self.post_data = {"external_id": self.external_id}

    def test_customer_detail(self):
        customer = Customer.objects.create(
            user=self.user, name="test-name", email="test-email"
        )
        request = self.factory.get("")
        request.user = self.user
        view = CustomerViewSet.as_view({"get": "retrieve"})
        response = view(request, pk=customer.pk)
        self.assertEqual(response.status_code, 200)

    def test_customer_add_product(self):
        customer = Customer.objects.create(
            user=self.user, name="test-name", email="test-email"
        )
        request = self.factory.post("", self.post_data)
        request.user = self.user

        view = CustomerViewSet.as_view({"post": "add_product"})
        response = view(request, pk=customer.pk)

        self.assertEqual(response.status_code, 201)

    def test_customer_remove_product(self):
        customer = Customer.objects.create(
            user=self.user, name="test-name", email="test-email"
        )
        request = self.factory.post("", self.post_data)
        request.user = self.user

        view = CustomerViewSet.as_view({"post": "add_product"})
        response = view(request, pk=customer.pk)

        view = CustomerViewSet.as_view({"post": "remove_product"})
        response = view(request, pk=customer.pk)
        self.assertEqual(response.status_code, 200)
