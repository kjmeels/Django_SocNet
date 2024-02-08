from django.db import models
from django.db.models import UniqueConstraint


class News(models.Model):
    text = models.TextField(verbose_name="Текст", null=True, blank=True)
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
        return f"Новость {self.id} - {self.user.username}"

    class Meta:
        verbose_name: str = "Новость"
        verbose_name_plural: str = "Новости"


class Like(models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="users",
        verbose_name="Пользователь",
    )
    new = models.ForeignKey(
        "news.News",
        on_delete=models.CASCADE,
        related_name="news",
        verbose_name="Новости",
    )

    class Meta:
        verbose_name: str = "Лайк"
        verbose_name_plural: str = "Лайки"
        constraints = [UniqueConstraint(fields=("user", "new"), name="unique_user_new_together")]
