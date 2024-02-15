from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from languages.serializers import LanguageSerializer
from news.serializers import NewsSerializer
from .models import User, Photo, Music


class PhotoSerializer(serializers.ModelSerializer):
    """Сериализатор фотографий"""

    class Meta:
        model = Photo
        fields = ("photo",)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей."""

    user_photos = PhotoSerializer(many=True)
    city = serializers.SerializerMethodField()

    @extend_schema_field(serializers.CharField)
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


class AddPhotoSerializer(serializers.ModelSerializer):
    """Сериализатор добавления фото."""

    class Meta:
        model = Photo
        fields = (
            "id",
            "photo",
            "user",
        )


class CommonFriendsSerializer(serializers.Serializer):
    """Сериализатор общих друзей."""

    count = serializers.IntegerField()
    common_friends = serializers.SerializerMethodField()

    @extend_schema_field(UserFriendsSerializer(many=True))
    def get_common_friends(self, obj):
        return UserFriendsSerializer(self.context["common_friends"], many=True).data


class AddMusicSerializer(serializers.ModelSerializer):
    """Сериализатор на добавление музыки."""

    class Meta:
        model = Music
        fields = (
            # "file",
            "title",
            "author",
            "image",
        )
