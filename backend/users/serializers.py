from rest_framework import serializers

from languages.serializers import LanguageSerializer
from .models import User, Photo, News


class PhotoSerializer(serializers.ModelSerializer):
    """Сериализатор фотографий"""

    class Meta:
        model = Photo
        fields = ("photo",)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей."""

    user_photos = PhotoSerializer(many=True)
    city = serializers.SerializerMethodField()

    def get_city(self, obj):
        if obj.city:
            return obj.city.name
        return None

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


class UserFriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "full_name",
            "image",
        )


class UserRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя с новостями."""

    user_photos = PhotoSerializer(many=True)
    city = serializers.SerializerMethodField()
    languages = LanguageSerializer(many=True)
    user_news = NewsSerializer(many=True)
    friends = UserFriendsSerializer(many=True)

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
            "user_news",
            "friends",
        )

    def get_city(self, obj):
        if obj.city:
            return obj.city.name
        return None
