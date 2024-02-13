# Generated by Django 4.2.5 on 2024-02-12 09:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("news", "0003_like_unique_user_new_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="like",
            name="new",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="news",
                to="news.news",
                verbose_name="Новость",
            ),
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("text", models.TextField(verbose_name="Текст")),
                (
                    "added_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления"),
                ),
                (
                    "new",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="new_comment",
                        to="news.news",
                        verbose_name="Новость",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_comment",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Комментарий",
                "verbose_name_plural": "Комментарии",
            },
        ),
    ]
