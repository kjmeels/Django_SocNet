from rest_framework import serializers
from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Сериализатор уведомлений."""

    class Meta:
        model = Notification
        fields = (
            "id",
            "sender",
            "type",
            "receiver",
            "is_read",
        )
