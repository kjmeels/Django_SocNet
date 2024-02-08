# Generated by Django 4.2.5 on 2024-02-08 14:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("news", "0002_alter_news_text_like"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="like",
            constraint=models.UniqueConstraint(
                fields=("user", "new"), name="unique_user_new_together"
            ),
        ),
    ]
