from django.urls import reverse
from faker import Faker
from parameterized import parameterized
from rest_framework import status

from apps.accounts.factories import UserFactory
from apps.accounts.models import User
from apps.commons.test import JwtAPITestCase, TestRoles

faker = Faker()


class CreateUserTestCase(JwtAPITestCase):
    @parameterized.expand(
        [
            (TestRoles.ANONYMOUS, status.HTTP_201_CREATED),
            (TestRoles.DEFAULT, status.HTTP_201_CREATED),
            (TestRoles.ADMIN, status.HTTP_201_CREATED),
        ]
    )
    def test_create_user(self, role, expected_status):
        user = self.get_parameterized_test_user(role)
        self.client.force_authenticate(user)
        payload = {
            "username": faker.email(),
            "email": faker.email(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "password": faker.password(),
        }
        response = self.client.post(reverse("User-list"), payload)
        self.assertEqual(response.status_code, expected_status)
        if response.status_code == status.HTTP_201_CREATED:
            content = response.json()
            self.assertEqual(content["username"], payload["username"])
            self.assertEqual(content["email"], payload["email"])
            self.assertEqual(content["first_name"], payload["first_name"])
            self.assertEqual(content["last_name"], payload["last_name"])


class UpdateUserTestCase(JwtAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = UserFactory()

    @parameterized.expand(
        [
            (TestRoles.ANONYMOUS, status.HTTP_401_UNAUTHORIZED),
            (TestRoles.DEFAULT, status.HTTP_403_FORBIDDEN),
            (TestRoles.ADMIN, status.HTTP_200_OK),
            (TestRoles.OWNER, status.HTTP_200_OK),
        ]
    )
    def test_update_user(self, role, expected_status):
        user = self.get_parameterized_test_user(role, owned_instance=self.user)
        self.client.force_authenticate(user)
        payload = {
            "username": faker.email(),
            "email": faker.email(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
        }
        response = self.client.patch(
            reverse("User-detail", args=(self.user.id,)), payload
        )
        self.assertEqual(response.status_code, expected_status)
        if response.status_code == status.HTTP_201_CREATED:
            content = response.json()
            self.assertEqual(content["username"], payload["username"])
            self.assertEqual(content["email"], payload["email"])
            self.assertEqual(content["first_name"], payload["first_name"])
            self.assertEqual(content["last_name"], payload["last_name"])


class DeleteUserTestCase(JwtAPITestCase):
    @parameterized.expand(
        [
            (TestRoles.ANONYMOUS, status.HTTP_401_UNAUTHORIZED),
            (TestRoles.DEFAULT, status.HTTP_403_FORBIDDEN),
            (TestRoles.ADMIN, status.HTTP_204_NO_CONTENT),
            (TestRoles.OWNER, status.HTTP_204_NO_CONTENT),
        ]
    )
    def test_delete_user(self, role, expected_status):
        instance = UserFactory()
        user = self.get_parameterized_test_user(role, owned_instance=instance)
        self.client.force_authenticate(user)
        response = self.client.delete(reverse("User-detail", args=(instance.id,)))
        self.assertEqual(response.status_code, expected_status)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            self.assertFalse(User.objects.filter(id=instance.id).exists())


class ReadUserTestCase(JwtAPITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = UserFactory()

    @parameterized.expand(
        [
            (TestRoles.ANONYMOUS, status.HTTP_200_OK),
            (TestRoles.DEFAULT, status.HTTP_200_OK),
            (TestRoles.ADMIN, status.HTTP_200_OK),
        ]
    )
    def test_get_user(self, role, expected_status):
        user = self.get_parameterized_test_user(role)
        self.client.force_authenticate(user)
        response = self.client.get(reverse("User-detail", args=(self.user.id,)))
        self.assertEqual(response.status_code, expected_status)
        if response.status_code == status.HTTP_200_OK:
            content = response.json()
            self.assertEqual(content["username"], self.user.username)
            self.assertEqual(content["email"], self.user.email)
            self.assertEqual(content["first_name"], self.user.first_name)
            self.assertEqual(content["last_name"], self.user.last_name)

    @parameterized.expand(
        [
            (TestRoles.ANONYMOUS, status.HTTP_200_OK),
            (TestRoles.DEFAULT, status.HTTP_200_OK),
            (TestRoles.ADMIN, status.HTTP_200_OK),
        ]
    )
    def test_list_users(self, role, expected_status):
        user = self.get_parameterized_test_user(role)
        self.client.force_authenticate(user)
        response = self.client.get(reverse("User-list"))
        self.assertEqual(response.status_code, expected_status)
        if response.status_code == status.HTTP_200_OK:
            content = response.json()["results"]
            self.assertEqual(len(content), User.objects.count())
            self.assertSetEqual(
                {user["id"] for user in content},
                {user.id for user in User.objects.all()},
            )
