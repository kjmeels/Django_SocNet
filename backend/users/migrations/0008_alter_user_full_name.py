# Generated by Django 4.2.5 on 2024-02-01 10:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0007_alter_news_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="full_name",
            field=models.CharField(max_length=50, verbose_name="Псевдоним"),
        ),
    ]