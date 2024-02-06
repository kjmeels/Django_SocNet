from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from news.models import News
from news.serializers import AddNewsSerializer, GetNewsSerializer


class NewsViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    """ViewSet новостей"""

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return AddNewsSerializer
        elif self.action == "list":
            return GetNewsSerializer

    def get_queryset(self):
        return (
            News.objects.all()
            .select_related("user")
            .filter(
                user__in=[
                    self.request.user.id,
                    *self.request.user.friends.values_list("id", flat=True),
                ]
            )
        )
