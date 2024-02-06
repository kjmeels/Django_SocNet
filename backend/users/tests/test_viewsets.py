from functools import partial

from django.urls import reverse
from pytest import mark
from rest_framework import status
from rest_framework.test import APITestCase

from languages.tests.factories import LanguageFactory
from .factories import UserFactory, PhotoFactory, NewsFactory
from ..models import News, Photo


@mark.django_db
class TestUserViewSet(APITestCase):
    def setUp(self):
        self.list_url: str = reverse("users-list")
        self.detail_url = partial(reverse, "users-detail")
        self.get_my_page_url: str = reverse("users-get-my-page")
        self.add_news_url: str = reverse("users-create-news")
        self.add_photo_url: str = reverse("users-create-photo")
        self.get_news: str = reverse("users-get-news")

    def test_user_list(self):
        users = [UserFactory() for _ in range(5)]
        users_photo = [PhotoFactory(user=user) for user in users for _ in range(5)]
        languages = [LanguageFactory() for _ in range(5)]
        for user in users:
            user.languages.set(languages)

        self.client.force_authenticate(user=users[0])

        with self.assertNumQueries(3):
            res = self.client.get(self.list_url)

        res_json = res.json()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_json), len(users))
        self.assertEqual(len(res_json[0]["user_photos"]), len(users_photo) / len(users))
        self.assertEqual(len(res_json[0]["languages"]), len(languages))

    def test_user_retrieve(self):
        users = [UserFactory() for _ in range(5)]
        users_photo = [PhotoFactory(user=user) for user in users for _ in range(5)]
        languages = [LanguageFactory() for _ in range(5)]
        user_news = [NewsFactory(user=user) for user in users for _ in range(5)]
        user_friends = [UserFactory() for _ in range(10)]

        for user in users:
            user.languages.set(languages)
            user.friends.set(user_friends)

        self.client.force_authenticate(user=users[0])

        with self.assertNumQueries(5):
            res = self.client.get(self.detail_url(kwargs={"pk": users[2].id}))

        res_json = res.json()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res_json["id"], users[2].id)
        self.assertEqual(len(res_json["user_photos"]), len(users_photo) / len(users))
        self.assertEqual(len(res_json["languages"]), len(languages))
        self.assertEqual(len(res_json["user_news"]), len(user_news) / len(users))
        self.assertEqual(len(res_json["friends"]), len(user_friends))

    def test_my_page(self):
        user = UserFactory()
        user_photos = [PhotoFactory(user=user) for _ in range(10)]
        languages = [LanguageFactory() for _ in range(10)]
        user_news = [NewsFactory(user=user) for _ in range(10)]
        user_friends = [UserFactory() for _ in range(10)]

        user.languages.set(languages)
        user.friends.set(user_friends)

        with self.assertNumQueries(0):
            res = self.client.get(self.get_my_page_url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=user)

        with self.assertNumQueries(5):
            res = self.client.get(self.get_my_page_url)

        res_json = res.json()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res_json["id"], user.pk)
        self.assertEqual(len(res_json["user_photos"]), len(user_photos))
        self.assertEqual(len(res_json["languages"]), len(languages))
        self.assertEqual(len(res_json["user_news"]), len(user_news))
        self.assertEqual(len(res_json["friends"]), len(user_friends))

    def test_add_news(self):
        user = UserFactory()
        payload = {
            "text": "new news",
            "user": user.pk,
            "created_at": "06.02.2024",
            "image": "",
        }

        with self.assertNumQueries(0):
            res = self.client.post(self.add_news_url, data=payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=user)

        with self.assertNumQueries(2):
            res = self.client.post(self.add_news_url, data=payload)

        res_json = res.json()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_json["user"], user.pk)
        self.assertEqual(News.objects.count(), 1)

    def test_add_photo(self):
        user = UserFactory()
        payload = {
            "photo": "",
            "user": user.pk,
        }

        with self.assertNumQueries(0):
            res = self.client.post(self.add_photo_url, data=payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=user)

        with self.assertNumQueries(2):
            res = self.client.post(self.add_photo_url, data=payload)

        res_json = res.json()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_json["user"], user.pk)
        self.assertEqual(Photo.objects.count(), 1)

    def test_get_news(self):
        users = [UserFactory() for _ in range(10)]
        user_news = [NewsFactory(user=user) for user in users for _ in range(10)]

        self.client.force_authenticate(user=users[0])

        users[0].friends.set(users[1:5])

        with self.assertNumQueries(2):
            res = self.client.get(self.get_news)

        res_json = res.json()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(res_json), len(user_news) / len(users) * (users[0].friends.count() + 1)
        )
