from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import User
from .serializers import UserSerializer, UserRetrieveSerializer


class UserViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    """ViewSet пользователя"""

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserRetrieveSerializer
        elif self.action == "get_my_page":
            return UserRetrieveSerializer
        return UserSerializer

    def get_queryset(self):
        if self.action in ["retrieve", "get_my_page"]:
            return (
                User.objects.all()
                .prefetch_related("user_photos", "languages", "user_news")
                .select_related("city")
            )
        return (
            User.objects.all().prefetch_related("user_photos", "languages").select_related("city")
        )

    @action(detail=False, methods=["GET"])
    def get_my_page(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            queryset = self.get_queryset().filter(id=self.request.user.id).first()
            serializer = self.get_serializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
