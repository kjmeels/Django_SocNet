from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей."""

    languages = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "full_name", "image", "city", "age", "gender", "birth_date", "languages")

    def get_languages(self, obj):
        return obj.languages.values_list("language_name", flat=True)
