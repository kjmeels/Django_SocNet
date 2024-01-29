from rest_framework import serializers

from .models import User, News


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей."""

    class Meta:
        model = User
        fields = (
            "id",
            "full_name",
            "image",
            "city",
            "age",
            "gender",
            "birth_date",
        )


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
