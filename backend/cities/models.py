from django.db import models


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название города")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name: str = "Город"
        verbose_name_plural: str = "Города"
