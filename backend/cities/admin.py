from django.contrib.admin import register, ModelAdmin

from .models import City


@register(City)
class CityAdmin(ModelAdmin):
    pass
