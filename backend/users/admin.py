from django.contrib.admin import register, ModelAdmin
from django.contrib.auth.admin import UserAdmin

from .models import User, News


@register(User)
class UserAdmin(UserAdmin):
    pass


@register(News)
class NewsAdmin(ModelAdmin):
    pass
