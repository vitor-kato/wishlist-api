from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="test-user", password="")

    def test_user_login(self):
        c = Client()
        new_password = "test-password"
        user = User.objects.get(username="test-user")
        user.set_password(new_password)
        user.save()

        response = c.post(
            "/api/token/", {"username": "test-user", "password": new_password}
        )

        self.assertEqual(response.status_code, 200)
