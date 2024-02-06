from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import User
from .serializers import (
    UserSerializer,
    UserRetrieveSerializer,
    AddNewsSerializer,
    AddPhotoSerializer,
)


class UserViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet
):
    """ViewSet пользователя"""

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserRetrieveSerializer
        elif self.action == "get_my_page":
            return UserRetrieveSerializer
        elif self.action == "create_news":  # ----------------------
            return AddNewsSerializer
        elif self.action == "create_photo":
            return AddPhotoSerializer
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

    @action(detail=False, methods=["POST"])
    def create_news(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=["POST"])
    def create_photo(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    # todo Добавить метод ПОСТ для добавления ностей и фотографий, (1. написать сериализатор на создание новостец и на создание фото 2.доавить экшены на ПОСТ методы 3. тесты)
    # todo Добавить АПИ для новостей (список нвостей друзей) - новостная лента
