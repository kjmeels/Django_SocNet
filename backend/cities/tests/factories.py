import factory
from factory.django import DjangoModelFactory

from ..models import City


class CityFactory(DjangoModelFactory):
    name = factory.Faker("word")

    class Meta:
        model = City
