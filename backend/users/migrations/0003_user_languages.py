# Generated by Django 4.2.5 on 2024-01-30 14:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("languages", "0001_initial"),
        ("users", "0002_user_age_user_birth_date_user_city_user_gender_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="languages",
            field=models.ManyToManyField(
                blank=True, related_name="users", to="languages.language", verbose_name="Языки"
            ),
        ),
    ]
