from django.contrib.admin import register, ModelAdmin

from .models import News


@register(News)
class NewsAdmin(ModelAdmin):
    pass
