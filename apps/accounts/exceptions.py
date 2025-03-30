from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class ExampleException(APIException):
    status_code = status
    default_detail = _("Example error")
    default_code = "example_error"
