import factory
from factory.django import DjangoModelFactory

from ..models import News, Like
from users.tests.factories import UserFactory


class NewsFactory(DjangoModelFactory):
    text = factory.Faker("word")
    user = factory.SubFactory(UserFactory)
    created_at = factory.Faker("date")
    image = factory.django.ImageField(filename="test.png")

    class Meta:
        model = News


class LikeFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    new = factory.SubFactory(NewsFactory)

    class Meta:
        model = Like
