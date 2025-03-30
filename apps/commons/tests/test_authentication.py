from django.urls import reverse
from faker import Faker
from rest_framework import status

from apps.accounts.factories import UserFactory
from apps.commons.test import JwtAPITestCase

faker = Faker()


class AuthenticationTestCase(JwtAPITestCase):
    def test_authentication(self):
        password = faker.password()
        user = UserFactory(password=password)
        payload = {
            "username": user.username,
            "password": password,
        }
        # Test token retrieval
        response = self.client.post(reverse("token_obtain_pair"), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = response.json()
        self.assertIn("access", content)
        # Test token refresh
        payload = {
            "refresh": content["refresh"],
        }
        response = self.client.post(reverse("token_refresh"), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = response.json()
        self.assertIn("access", content)
        # Test token verification
        self.client.force_authenticate(token=content["access"])
        payload = {
            "first_name": faker.first_name(),
        }
        response = self.client.patch(reverse("User-detail", args=(user.id,)), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = response.json()
        self.assertEqual(content["first_name"], payload["first_name"])
