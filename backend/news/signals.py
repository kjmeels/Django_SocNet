from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import News, Like
from notifications.constants import NotificationTypeChoice
from notifications.models import Notification, NotificationType
from notifications.tasks import send_email


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

    notifications = Notification.objects.bulk_create(objs=notification_list)
    for notification in notifications:
        send_email.delay(sender=notification.sender, receiver=notification.receiver)


@receiver(post_save, sender=Like)
def news_post_save(instance: Like, **kwargs):
    send_email.delay(instance.user)
