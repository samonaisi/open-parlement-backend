from django.db.models import Model
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: GenericViewSet) -> bool:
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(
        self, request: Request, view: GenericViewSet, instance: Model
    ) -> bool:
        return self.has_permission(request, view)
