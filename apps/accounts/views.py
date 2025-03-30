from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from apps.commons.permissions import ReadOnly

from .models import User
from .permissions import IsAccountOwner
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [ReadOnly | IsAccountOwner | IsAdminUser]
    serializer_class = UserSerializer
