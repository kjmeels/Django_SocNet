import factory
from factory.django import DjangoModelFactory

from ..models import News
from users.tests.factories import UserFactory


class NewsFactory(DjangoModelFactory):
    text = factory.Faker("word")
    user = factory.SubFactory(UserFactory)
    created_at = factory.Faker("date")
    image = factory.django.ImageField(filename="test.png")

    class Meta:
        model = News
