from django.db import models


class Language(models.Model):
    language_name = models.CharField(max_length=50, verbose_name="Язык", null=True, blank=True)

    def __str__(self):
        return self.language_name

    class Meta:
        verbose_name: str = "Язык"
        verbose_name_plural: str = "Языки"
