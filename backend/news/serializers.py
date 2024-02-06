from rest_framework import serializers

from users.models import User
from .models import News


class NewsSerializer(serializers.ModelSerializer):
    """Сериализатор новостей."""

    class Meta:
        model = News
        fields = (
            "user",
            "text",
            "created_at",
            "image",
        )


class AddNewsSerializer(serializers.ModelSerializer):
    """Сериализатор добавления новостей."""

    class Meta:
        model = News
        fields = (
            "id",
            "text",
            "user",
            "created_at",
            "image",
        )


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор профиля прользователя."""

    class Meta:
        model = User
        fields = (
            "id",
            "full_name",
            "image",
        )


class GetNewsSerializer(serializers.ModelSerializer):
    """Сериализатор на получение новостей (новостная лента)."""

    user = UserProfileSerializer()

    class Meta:
        model = News
        fields = (
            "text",
            "user",
            "created_at",
            "image",
        )
