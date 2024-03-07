from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from notifications.models import Notification
from notifications.serializer import NotificationSerializer


class NotificationViewSet(ReadOnlyModelViewSet):
    """ViewSet уведомлений."""

    permission_classes = [IsAuthenticated]

    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.select_related("receiver").filter(
            receiver=self.request.user, is_read=False
        )
