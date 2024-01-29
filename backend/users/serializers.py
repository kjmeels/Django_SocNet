from rest_framework import serializers

from users.models import User, Photo


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


class PhotoSerializer(serializers.ModelSerializer):
    """Сериализатор фотографий"""

    class Meta:
        model = Photo
        fields = (
            "photo",
            "user",
        )
