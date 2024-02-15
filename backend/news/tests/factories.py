import factory
from factory.django import DjangoModelFactory

from ..models import News, Like, Comment, CommentLike
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


class CommentFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    new = factory.SubFactory(NewsFactory)
    text = factory.Faker("word")
    added_at = factory.Faker("date")

    class Meta:
        model = Comment


class CommentLikeFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    comment = factory.SubFactory(CommentFactory)

    class Meta:
        model = CommentLike
