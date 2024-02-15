# Generated by Django 4.2.5 on 2024-02-15 14:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0011_delete_news"),
    ]

    operations = [
        migrations.CreateModel(
            name="Music",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        upload_to="u/m/f",
                        validators=[django.core.validators.FileExtensionValidator(("mp3",))],
                        verbose_name="Файл",
                    ),
                ),
                ("title", models.CharField(max_length=50, verbose_name="Название песни")),
                ("author", models.CharField(max_length=50, verbose_name="Исполнитель")),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="u/m/i", verbose_name="Обложка"
                    ),
                ),
            ],
            options={
                "verbose_name": "Песня",
                "verbose_name_plural": "Музыка",
            },
        ),
        migrations.AlterField(
            model_name="photo",
            name="photo",
            field=models.ImageField(blank=True, null=True, upload_to="u/p/p", verbose_name="Фото"),
        ),
    ]
