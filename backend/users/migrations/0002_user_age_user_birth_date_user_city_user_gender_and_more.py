# Generated by Django 4.2.5 on 2024-01-26 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Возраст'),
        ),
        migrations.AddField(
            model_name='user',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата рождения'),
        ),
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('Male', 'Мужчина'), ('Female', 'Женщина')], default='Male', max_length=50, verbose_name='Пол'),
        ),
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='u/u/i', verbose_name='Фото пользователя'),
        ),
    ]
