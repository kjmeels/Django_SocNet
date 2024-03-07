from django.db import models
from django.db.models import UniqueConstraint

from notifications.constants import NotificationTypeChoice


class Notification(models.Model):
    sender = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        related_name="notifications",
        verbose_name="Отправитель",
        null=True,
    )
    type = models.ForeignKey(
        "notifications.NotificationType",
        on_delete=models.SET_NULL,
        related_name="notifications",
        null=True,
    )
    receiver = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="Получатель",
        related_name="your_notifications",
    )
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")

    def __str__(self):
        return f"Уведомление от {self.sender.username}"

    class Meta:
        verbose_name: str = "Уведомление"
        verbose_name_plural: str = "Уведомления"


class NotificationType(models.Model):
    text = models.TextField(verbose_name="Текст уведомления")
    type = models.CharField(
        verbose_name="Тип", choices=NotificationTypeChoice.choices, max_length=30, unique=True
    )

    def __str__(self):
        return self.text if len(self.text) < 50 else self.text[:50]

    class Meta:
        verbose_name: str = "Тип уведомления"
        verbose_name_plural: str = "Тип уведомлений"
