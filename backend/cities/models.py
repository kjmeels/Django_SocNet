from django.db import models


class City(models.Model):
    city = models.CharField(max_length=50, verbose_name="Город", null=True, blank=True)  # true ?

    def __str__(self):  # для чего?
        return self.city

    class Meta:
        verbose_name: str = "Город"
        verbose_name_plural: str = "Города"
