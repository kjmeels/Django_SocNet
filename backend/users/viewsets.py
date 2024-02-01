from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .models import User
from .serializers import UserSerializer, UserNewsRetrieveSerializer


class UserViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    """ViewSet пользователя"""

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserNewsRetrieveSerializer
        return UserSerializer

    def get_queryset(self):
        if self.action == "retrieve":
            return (
                User.objects.all()
                .prefetch_related("user_photos", "languages", "user_news")
                .select_related("city")
            )
        return (
            User.objects.all().prefetch_related("user_photos", "languages").select_related("city")
        )
