from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import GenderChoices


class User(AbstractUser):
    full_name = models.CharField(max_length=50, verbose_name="Имя пользователя")
    image = models.ImageField(
        upload_to="u/u/i", verbose_name="Фото пользователя", null=True, blank=True
    )
    city = models.CharField(max_length=50, verbose_name="Город", null=True, blank=True)
    age = models.PositiveIntegerField(verbose_name="Возраст", null=True, blank=True)
    gender = models.CharField(
        max_length=50, verbose_name="Пол", choices=GenderChoices.choices, default=GenderChoices.MALE
    )
    birth_date = models.DateField(verbose_name="Дата рождения", null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name: str = "Пользователь"
        verbose_name_plural: str = "Пользователи"


class Photo(models.Model):
    photo = models.ImageField(upload_to="u/u/p", verbose_name="Фото", null=True, blank=True)
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="user_photos",
        verbose_name="Пользователь",
    )

    def __str__(self):
        return f"photo {self.user.username} - {self.id}"

    class Meta:
        verbose_name: str = "Фотография"
        verbose_name_plural: str = "Фотографии"
