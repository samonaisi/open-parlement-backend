from __future__ import annotations

import base64
import logging
from typing import Dict, List, Optional
from unittest import util

from django.conf import settings
from django.core.files import File
from django.db import models
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from apps.accounts.factories import UserFactory
from apps.accounts.models import User

from .exceptions import ExceptionType
from .mixins import HasOwnerMixin

util._MAX_LENGTH = 1000000


class TestRoles(models.TextChoices):
    ANONYMOUS = "anonymous"
    DEFAULT = "default"
    ADMIN = "admin"
    OWNER = "owner"


class JwtClient(APIClient):
    """
    Override default `Client` to create a Token when `force_authenticate` is called.
    This token will then be given in any subsequent request in the header.
    """

    def force_authenticate(  # nosec
        self,
        user: Optional[User] = None,
        token: Optional[str] = None,
    ):
        """Login the given user by creating a JWT token."""
        token_type = "Bearer"  # nosec
        if user and not token:
            token = AccessToken.for_user(user)
        if token:
            self.credentials(HTTP_AUTHORIZATION=f"{token_type} {token}")


class JwtAPITestCase(APITestCase):
    """`APITestCase` using `JwtClient`."""

    client: JwtClient
    client_class = JwtClient

    @classmethod
    def setUpClass(cls):
        """Disable logging while testing."""
        super().setUpClass()
        logging.disable(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        """Re-enable logging after testing."""
        super().tearDownClass()
        logging.disable(logging.NOTSET)

    def tearDown(self):
        """Logout any authentication at the end of each test."""
        super().tearDown()
        self.client.logout()
        self.client.credentials()

    @classmethod
    def get_parameterized_test_user(
        cls, role: TestRoles, owned_instance: Optional[HasOwnerMixin] = None
    ) -> Optional[User]:
        if role == TestRoles.OWNER and not owned_instance:
            raise ValueError("Owned instance must be provided for OWNER role")
        if role == TestRoles.OWNER:
            return owned_instance.get_owner()
        if role == TestRoles.ANONYMOUS:
            return None
        if role == TestRoles.DEFAULT:
            return UserFactory()
        if role == TestRoles.ADMIN:
            return UserFactory(is_staff=True)
        return None

    @classmethod
    def get_test_image_file(cls) -> File:
        """Return a dummy test image file."""
        return File(
            open(f"{settings.STATIC_ROOT}/test_image.png", "rb")  # noqa: SIM115
        )

    @classmethod
    def get_base64_image(cls) -> str:
        return f'<img src="data:image/png;base64,{base64.b64encode(cls.get_test_image_file().read()).decode()}" alt=""/>'

    def assertApiValidationError(  # noqa: N802
        self, response, messages: Optional[Dict[str, List[str]]] = None
    ):
        content = response.json()
        self.assertEqual(content["type"], ExceptionType.VALIDATION.value)
        if messages:
            self.assertEqual(content["errors"], messages)

    def assertApiPermissionError(  # noqa: N802
        self, response, detail: Optional[str] = None
    ):
        content = response.json()
        self.assertEqual(content["type"], ExceptionType.PERMISSION.value)
        if detail:
            self.assertEqual(content["detail"], detail)

    def assertApiTechnicalError(  # noqa: N802
        self, response, detail: Optional[str] = None
    ):
        content = response.json()
        self.assertEqual(content["type"], ExceptionType.TECHNICAL.value)
        if detail:
            self.assertEqual(content["detail"], detail)

    def assertApiAuthenticationError(  # noqa: N802
        self, response, detail: Optional[str] = None
    ):
        content = response.json()
        self.assertEqual(content["type"], ExceptionType.AUTHENTHICATION.value)
        if detail:
            self.assertEqual(content["detail"], detail)
