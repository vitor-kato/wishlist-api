import unittest

from customers.models import Customer
from django.test import TestCase

from config.base_models import User

from .client import ProductClient
from .models import Product, Wishlist


class WishlistTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test-user", password="")

    def test_customer_signal_creates_wishlist(self):
        customer = Customer.objects.create(
            user=self.user, name="test-name", email="test-email"
        )
        self.assertEqual(isinstance(customer.wishlist, Wishlist), True)

    def test_product_client_success(self):
        id = "571fa8cc-2ee7-5ab4-b388-06d55fd8ab2f"
        c = ProductClient(id)
        c.get_data()
        self.assertEqual(c.status, 200)

    @unittest.expectedFailure
    def test_product_client_failure(self):
        id = "xxxxxxxxxxx"
        c = ProductClient(id)
        c.get_data()

    def test_add_product_to_wishlist(self):
        id = "571fa8cc-2ee7-5ab4-b388-06d55fd8ab2f"
        customer = Customer.objects.create(
            user=self.user, name="test-name", email="test-email"
        )
        wishlist = customer.wishlist
        product = Product.objects.create(external_id=id)
        product.wishlist.add(wishlist)
