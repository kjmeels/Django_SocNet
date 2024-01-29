from django.db.models import TextChoices


class GenderChoices(TextChoices):
    MALE = "Male", "Мужчина"
    FEMALE = "Female", "Женщина"
