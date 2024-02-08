from django.db import IntegrityError
from django.urls import reverse
from pytest import mark
from rest_framework import status
from rest_framework.test import APITestCase

from news.tests.factories import NewsFactory, LikeFactory
from .factories import UserFactory
from ..models import News, Like


@mark.django_db
class TestNewsViewSet(APITestCase):
    def setUp(self):
        self.list_url: str = reverse("news-list")
        self.add_like_url: str = reverse("news-add-like")
        self.destroy_like_url: str = reverse("news-destroy-like")

    def test_create(self):
        user = UserFactory()
        payload = {
            "text": "new news",
            "user": user.pk,
            "created_at": "06.02.2024",
            "image": "",
        }

        with self.assertNumQueries(0):
            res = self.client.post(self.list_url, data=payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=user)

        with self.assertNumQueries(2):
            res = self.client.post(self.list_url, data=payload)

        res_json = res.json()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_json["user"], user.pk)
        self.assertEqual(News.objects.count(), 1)

    def test_list(self):
        users = [UserFactory() for _ in range(10)]
        user_news = [NewsFactory(user=user) for user in users for _ in range(10)]

        self.client.force_authenticate(user=users[0])

        users[0].friends.set(users[1:5])

        with self.assertNumQueries(2):
            res = self.client.get(self.list_url)

        res_json = res.json()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(res_json), len(user_news) / len(users) * (users[0].friends.count() + 1)
        )

    def test_add_like(self):
        user = UserFactory()
        new = NewsFactory()

        self.client.force_authenticate(user=user)

        with self.assertNumQueries(2):
            res = self.client.post(self.add_like_url, data={"new": new.pk})

        res_json = res.json()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_json["new"], new.pk)
        self.assertEqual(Like.objects.count(), 1)

        try:
            with self.assertNumQueries(2):
                res = self.client.post(self.add_like_url, data={"new": new.pk})
        except IntegrityError:
            pass
        except Exception:
            self.fail("Не отработал UniqueConstraint")

    def test_destroy_like(self):
        user = UserFactory()
        new = NewsFactory()
        like = LikeFactory(user=user, new=new)

        self.client.force_authenticate(user=user)

        with self.assertNumQueries(2):
            res = self.client.delete(f"{self.destroy_like_url}?new={new.pk}")

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Like.objects.count(), 0)
