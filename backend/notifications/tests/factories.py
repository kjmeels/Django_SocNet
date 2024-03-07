from factory import SubFactory, fuzzy, Faker
from factory.django import DjangoModelFactory

from notifications.constants import NotificationTypeChoice
from notifications.models import Notification, NotificationType
from users.tests.factories import UserFactory


class NotificationTypeFactory(DjangoModelFactory):
    type = fuzzy.FuzzyChoice(choices=NotificationTypeChoice.values)
    text = Faker("word")

    class Meta:
        model = NotificationType


class NotificationFactory(DjangoModelFactory):
    sender = SubFactory(UserFactory)
    type = SubFactory(NotificationTypeFactory)
    receiver = SubFactory(UserFactory)
    is_read = False

    class Meta:
        model = Notification
