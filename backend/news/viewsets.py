from django.db.models import Count, Prefetch
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django_filters import rest_framework as filters

from news.filters import NewFilter
from news.models import News, Like, Comment, CommentLike
from news.serializers import (
    AddNewsSerializer,
    GetNewsSerializer,
    AddLikeSerializer,
    AddCommentSerializer,
    GetNewsDetailSerializer,
    AddLikeToCommentSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="Получить список новостей",
    ),
    create=extend_schema(
        summary="Добавление новой новости",
    ),
    add_like=extend_schema(
        summary="Добавление лайка",
    ),
    add_comment=extend_schema(
        summary="Добавление комментария",
    ),
    destroy_comment=extend_schema(
        summary="Удаление лайка",
    ),
    retrieve=extend_schema(
        summary="Получение определенной новости",
    ),
    destroy_like=extend_schema(summary="Удаление лайка"),
    destroy=extend_schema(
        summary="Удаление определенной новости",
    ),
)
@extend_schema(tags=["News"])
class NewsViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    """ViewSet новостей"""

    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = NewFilter

    def get_serializer_class(self):
        if self.action == "create":
            return AddNewsSerializer
        elif self.action == "list":
            return GetNewsSerializer
        elif self.action == "add_like":
            return AddLikeSerializer
        elif self.action == "add_comment":
            return AddCommentSerializer
        elif self.action == "retrieve":
            return GetNewsDetailSerializer
        elif self.action == "add_like_to_comment":
            return AddLikeToCommentSerializer

    def get_queryset(self):
        if self.action == "destroy_like":
            return Like.objects.filter(user=self.request.user.id)
        elif self.action == "destroy_comment":
            return Comment.objects.filter(user=self.request.user.id)
        elif self.action == "destroy_like_to_comment":
            return CommentLike.objects.filter(user=self.request.user.id)
        elif self.action == "retrieve":
            return (
                News.objects.all()
                .select_related("user")
                .prefetch_related(
                    Prefetch(
                        "comments",
                        Comment.objects.all()
                        .select_related("user")
                        .annotate(comment_like_count=Count("comment_likes")),
                    )
                )
                .annotate(like_count=Count("likes"))
                .filter(
                    user__in=[
                        self.request.user.id,  # берем новости пользователя
                        *self.request.user.friends.values_list(
                            "id", flat=True
                        ),  # берем новости его друзей
                    ]
                )
            )
        return (
            News.objects.all()
            .select_related("user")
            .annotate(comment_count=Count("comments"))
            .annotate(like_count=Count("likes"))
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

    @action(detail=False, methods=["POST"])
    def add_comment(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=["DELETE"])
    def destroy_comment(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=kwargs["pk"])
        if instance:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["POST"])
    def add_like_to_comment(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="comment", description="Комментарий", required=True, type=OpenApiTypes.INT
            )
        ]
    )
    @action(detail=False, methods=["DELETE"])
    def destroy_like_to_comment(self, request, *args, **kwargs):
        instance = self.get_queryset().filter(comment=request.query_params.get("comment")).first()
        if instance:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
