from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from news.models import News, Like
from news.serializers import AddNewsSerializer, GetNewsSerializer, AddLikeSerializer


@extend_schema(tags=["News"])
class NewsViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet
):
    """ViewSet новостей"""

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return AddNewsSerializer
        elif self.action == "list":
            return GetNewsSerializer
        elif self.action == "add_like":
            return AddLikeSerializer

    def get_queryset(self):
        if self.action == "destroy_like":
            return Like.objects.filter(user=self.request.user.id)
        return (
            News.objects.all().select_related("user")
            # .annotate(count("likes"))                          ?????????????
            .filter(
                user__in=[
                    self.request.user.id,
                    *self.request.user.friends.values_list("id", flat=True),
                ]
            )
        )

    @action(detail=False, methods=["POST"])
    def add_like(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="new", description="Новость", required=True, type=OpenApiTypes.INT
            )
        ]
    )
    @action(detail=False, methods=["DELETE"])
    def destroy_like(self, request, *args, **kwargs):
        instance = self.get_queryset().filter(new=request.query_params.get("new")).first()
        if instance:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


# todo Likes 1. создать модель с полями (фк на новость, фк на пользователя), 2. сериализатор на создание и удаление лайков 3.во вьюсете добавиьб 2 экшена на создание (пост)и удаение (делит) 4 тесты
# todo почитать про Constrains unique и про валидацию данных в сериализаторах (def ..._validate)

# UniqueConstraint создает уникальные ограничения , в нашем случае гарантирует, что пользователь сможет ставить только один лайк на каждую новость
