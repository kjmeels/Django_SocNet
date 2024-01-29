from django.contrib.admin import register, ModelAdmin

from .models import Language


@register(Language)
class LanguageAdmin(ModelAdmin):
    pass
