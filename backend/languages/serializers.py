from rest_framework import serializers

from .models import Language


class LanguageSerializer(serializers.ModelSerializer):
    """Сериализатор языка"""

    class Meta:
        model = Language
        fields = ("language_name",)
