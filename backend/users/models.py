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


class News(models.Model):
    text = models.TextField(verbose_name="Добавить новость", null=True, blank=True)
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="user_news",
        verbose_name="Пользователь",
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    image = models.ImageField(upload_to="u/u/n", verbose_name="Фото", null=True, blank=True)

    def __str__(self):
        return f" Новость {self.user.username} - {self.id}"

    class Meta:
        verbose_name: str = "Новость"
        verbose_name_plural: str = "Новости"
