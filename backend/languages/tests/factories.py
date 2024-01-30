import factory
from factory.django import DjangoModelFactory

from ..models import Language


class LanguageFactory(DjangoModelFactory):
    language_name = factory.Faker("word")

    class Meta:
        model = Language
