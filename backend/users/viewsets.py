from django.db.models import Prefetch, Count
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from news.models import News
from .models import User
from .serializers import (
    UserSerializer,
    UserRetrieveSerializer,
    AddPhotoSerializer,
    CommonFriendsSerializer,
    UserFriendsSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="Получить список ползователей",
    ),
    create=extend_schema(
        summary="Добавление нового пользователя",
    ),
    get_my_page=extend_schema(
        summary="Просмотр 'Моей страницы'",
    ),
    create_photo=extend_schema(
        summary="Добавление фото",
    ),
    retrieve=extend_schema(
        summary="Просмотр определеннго пользователя",
    ),
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
        elif self.action == "create_photo":
            return AddPhotoSerializer
        elif self.action == "get_common_friends":
            return CommonFriendsSerializer
        return UserSerializer

    def get_queryset(self):
        if self.action in ["retrieve", "get_my_page"]:
            return (
                User.objects.all()
                .prefetch_related(
                    "user_photos",
                    "languages",
                    Prefetch("user_news", News.objects.all().annotate(like_count=Count("news"))),
                )
                .select_related("city")
            )
        elif self.action == "get_common_friends":
            return User.objects.all().prefetch_related("friends")
        return (
            User.objects.all().prefetch_related("user_photos", "languages").select_related("city")
        )

    @action(detail=False, methods=["GET"])
    def get_my_page(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(id=self.request.user.id).first()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def create_photo(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="user", description="Пользователь", required=True, type=OpenApiTypes.INT
            )
        ],
    )
    @action(detail=False, methods=["GET"])
    def get_common_friends(self, request, *args, **kwargs):
        me = self.get_queryset().filter(id=self.request.user.id).first()
        person = self.get_queryset().filter(id=self.request.query_params.get("user")).first()

        me_friends = set(me.friends.all().values_list("id", flat=True))
        person_friends = set(person.friends.all().values_list("id", flat=True))

        common_friends_ids = person_friends & me_friends
        common_friends = self.get_queryset().filter(id__in=common_friends_ids)
        data = {"count": len(common_friends_ids)}
        serializer = self.get_serializer(data=data, context={"common_friends": common_friends})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
