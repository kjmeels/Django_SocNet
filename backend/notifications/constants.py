from django.db.models import TextChoices


class NotificationTypeChoice(TextChoices):
    NEW = "new", "добавил новость"
    FRIEND = "friend", "добавил друга"
    PHOTO = "photo", "добавил фото"
