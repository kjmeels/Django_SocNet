from django.contrib.admin import register, ModelAdmin  # верный импорт?

from .models import City


@register(City)
class CityAdmin(ModelAdmin):
    pass
