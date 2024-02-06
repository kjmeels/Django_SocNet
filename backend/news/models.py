from django.db import models


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
        return f"Новость {self.id} - {self.user.username}"

    class Meta:
        verbose_name: str = "Новость"
        verbose_name_plural: str = "Новости"
