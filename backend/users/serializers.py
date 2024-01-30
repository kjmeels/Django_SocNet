from rest_framework import serializers

from languages.serializers import LanguageSerializer
from .models import User, Photo


class PhotoSerializer(serializers.ModelSerializer):
    """Сериализатор фотографий"""

    class Meta:
        model = Photo
        fields = ("photo",)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей."""

    user_photos = PhotoSerializer(many=True)
    city = serializers.CharField(source="city.name")

    languages = LanguageSerializer(many=True)

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
            "user_photos",
            "languages",
        )
