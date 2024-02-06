from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import User, News
from .serializers import (
    UserSerializer,
    UserRetrieveSerializer,
    AddNewsSerializer,
    AddPhotoSerializer,
    GetNewsSerializer,
)


class UserViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet
):
    """ViewSet пользователя"""

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserRetrieveSerializer
        elif self.action == "get_my_page":
            return UserRetrieveSerializer
        elif self.action == "create_news":  # ----------------------
            return AddNewsSerializer
        elif self.action == "create_photo":
            return AddPhotoSerializer
        elif self.action == "get_news":
            return GetNewsSerializer
        return UserSerializer

    def get_queryset(self):
        if self.action in ["retrieve", "get_my_page"]:
            return (
                User.objects.all()
                .prefetch_related("user_photos", "languages", "user_news")
                .select_related("city")
            )
        elif self.action == "get_news":
            return News.objects.all().select_related("user")
        return (
            User.objects.all().prefetch_related("user_photos", "languages").select_related("city")
        )

    @action(detail=False, methods=["GET"])
    def get_my_page(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(id=self.request.user.id).first()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def create_news(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=["POST"])
    def create_photo(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=["GET"])
    def get_news(self, request, *args, **kwargs):
        # friends_queryset = User.objects.filter(id__in=self.request.user.friends.all())
        queryset = self.get_queryset().filter(
            user__in=[self.request.user.id, *self.request.user.friends.values_list("id", flat=True)]
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # todo Добавить метод ПОСТ для добавления ностей и фотографий, (1. написать сериализатор на создание новостец и на создание фото 2.доавить экшены на ПОСТ методы 3. тесты)
    # todo Добавить АПИ для новостей (список нвостей друзей) - новостная лента
