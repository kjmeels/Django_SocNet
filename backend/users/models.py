from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models

from .constants import GenderChoices


class User(AbstractUser):
    full_name = models.CharField(max_length=50, verbose_name="Псевдоним")
    image = models.ImageField(
        upload_to="u/u/i", verbose_name="Фото пользователя", null=True, blank=True
    )
    city = models.ForeignKey(
        "cities.City",
        on_delete=models.SET_NULL,
        verbose_name="Город",
        related_name="users",
        null=True,
        blank=True,
    )
    age = models.PositiveIntegerField(verbose_name="Возраст", null=True, blank=True)
    gender = models.CharField(
        max_length=50, verbose_name="Пол", choices=GenderChoices.choices, default=GenderChoices.MALE
    )
    birth_date = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    languages = models.ManyToManyField(
        "languages.Language", verbose_name="Языки", related_name="users", blank=True
    )
    friends = models.ManyToManyField(
        "users.User",
        verbose_name="Друзья",
        related_name="user_friends",
        blank=True,
    )
    music = models.ManyToManyField(
        "users.Music", verbose_name="Моя музыка", related_name="users", blank=True
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name: str = "Пользователь"
        verbose_name_plural: str = "Пользователи"


class Photo(models.Model):
    photo = models.ImageField(upload_to="u/p/p", verbose_name="Фото", null=True, blank=True)
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


class Music(models.Model):
    file = models.FileField(
        upload_to="u/m/f",
        verbose_name="Файл",
        validators=[FileExtensionValidator(("mp3",))],
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=50, verbose_name="Название песни")
    author = models.CharField(max_length=50, verbose_name="Исполнитель")
    image = models.ImageField(upload_to="u/m/i", verbose_name="Обложка", null=True, blank=True)

    def __str__(self):
        return f"file {self.title} - {self.author}"

    class Meta:
        verbose_name: str = "Песня"
        verbose_name_plural: str = "Музыка"
