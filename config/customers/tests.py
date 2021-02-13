import unittest

from django.test import TestCase

from config.base_models import User

from .models import Customer


class CustomerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test-user", password="")
        Customer.objects.create(user=self.user, name="test-name", email="test-email")

    @unittest.expectedFailure
    def test_duplicate_email(self):
        Customer.objects.create(user=self.user, name="test-name", email="test-email")
