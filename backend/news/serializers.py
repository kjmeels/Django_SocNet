from rest_framework import serializers

from users.models import User
from .models import News, Like, Comment


class NewsSerializer(serializers.ModelSerializer):
    """Сериализатор новостей."""

    like_count = serializers.IntegerField()

    class Meta:
        model = News
        fields = (
            "user",
            "text",
            "created_at",
            "image",
            "like_count",
        )


class AddNewsSerializer(serializers.ModelSerializer):
    """Сериализатор добавления новостей."""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

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
    like_count = serializers.IntegerField()

    class Meta:
        model = News
        fields = (
            "text",
            "user",
            "created_at",
            "image",
            "like_count",
        )


class AddLikeSerializer(serializers.ModelSerializer):
    """Сериализатор на добавление лайков."""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Like
        fields = (
            "user",
            "new",
        )


class AddCommentSerializer(serializers.ModelSerializer):
    """Сериализатор на добавление комментария."""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = (
            "user",
            "new",
            "text",
            "added_at",
        )


class GetCommentSerializer(serializers.ModelSerializer):
    """Сериализатор на получение комментариев новости."""

    user = UserProfileSerializer()

    class Meta:
        model = Comment
        fields = (
            "user",
            "id",
            "text",
            "added_at",
        )


class GetNewsDetailSerializer(serializers.ModelSerializer):
    """Сериализатор получения деталки новости."""

    user = UserProfileSerializer()
    like_count = serializers.IntegerField()
    comments = GetCommentSerializer(many=True)

    class Meta:
        model = News
        fields = (
            "text",
            "user",
            "created_at",
            "image",
            "like_count",
            "comments",
        )
