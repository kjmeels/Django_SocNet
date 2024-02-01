import factory
from factory import fuzzy
from factory.django import DjangoModelFactory

from cities.tests.factories import CityFactory
from ..constants import GenderChoices
from ..models import User, Photo, News


class UserFactory(DjangoModelFactory):
    username = factory.Sequence(lambda x: f"user_{x}")
    full_name = factory.Faker("word")
    image = factory.django.ImageField(filename="test.png")
    city = factory.SubFactory(CityFactory)
    age = factory.Faker("pyint", min_value=0, max_value=99)
    gender = fuzzy.FuzzyChoice(choices=GenderChoices.values)
    birth_date = factory.Faker("date")

    class Meta:
        model = User


class PhotoFactory(DjangoModelFactory):
    photo = factory.django.ImageField(filename="test.png")
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Photo


class NewsFactory(DjangoModelFactory):
    text = factory.Faker("word")
    user = factory.SubFactory(UserFactory)
    created_at = factory.Faker("date")
    image = factory.django.ImageField(filename="test.png")

    class Meta:
        model = News
