import factory
from factory.django import DjangoModelFactory

from ..models import City


class CityFactory(DjangoModelFactory):
    name = factory.Faker("word")
    slug = factory.Sequence(lambda n: f"slug_{n}")

    class Meta:
        model = City
