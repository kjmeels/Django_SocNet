from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet

from .models import User
from .serializers import UserSerializer


class UserViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    """ViewSet пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
