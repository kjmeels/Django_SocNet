from django.db.models.signals import post_save
from django.dispatch import receiver

from news.models import News
from notifications.constants import NotificationTypeChoice
from notifications.models import Notification, NotificationType


@receiver(post_save, sender=News)
def news_post_save(instance: News, **kwargs):
    notification_list = []
    for friend in instance.user.friends.all():
        notification = Notification(
            sender=instance.user,
            type=NotificationType.objects.filter(type=NotificationTypeChoice.NEW).first(),
            receiver=friend,
        )
        notification_list.append(notification)

    Notification.objects.bulk_create(objs=notification_list)
