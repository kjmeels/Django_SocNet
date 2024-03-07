from django.contrib.admin import register, ModelAdmin

from .models import Notification, NotificationType


@register(Notification)
class NotificationAdmin(ModelAdmin):
    pass


@register(NotificationType)
class NotificationTypeAdmin(ModelAdmin):
    pass
