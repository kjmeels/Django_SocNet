from django.contrib.admin import register, ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, Photo, Music


@register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    ("first_name", "last_name", "full_name"),
                    "image",
                    "birth_date",
                    "city",
                    "languages",
                    "age",
                    "gender",
                    "friends",
                )
            },
        ),
        (
            _("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )


@register(Photo)
class PhotoAdmin(ModelAdmin):
    pass


@register(Music)
class MusicAdmin(ModelAdmin):
    pass
