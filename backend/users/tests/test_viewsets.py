from functools import partial

from django.urls import reverse
from pytest import mark
from rest_framework import status
from rest_framework.test import APITestCase

from cities.tests.factories import CityFactory
from languages.tests.factories import LanguageFactory
from news.tests.factories import NewsFactory
from .factories import UserFactory, PhotoFactory, MusicFactory
from ..models import Photo, Music, User


@mark.django_db
class TestUserViewSet(APITestCase):
    def setUp(self):
        self.list_url: str = reverse("users-list")
        self.detail_url = partial(reverse, "users-detail")
        self.get_my_page_url: str = reverse("users-get-my-page")
        self.add_photo_url: str = reverse("users-create-photo")
        self.get_common_friends_url: str = reverse("users-get-common-friends")
        self.add_music_url: str = reverse("users-add-music")
        self.get_music_url: str = reverse("users-get-music")
        self.get_user_music_url: str = reverse("users-get-user-music")
        self.add_music_to_user_url: str = reverse("users-add-music-to-user")

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

        with self.assertNumQueries(6):
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

        with self.assertNumQueries(6):
            res = self.client.get(self.get_my_page_url)

        res_json = res.json()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res_json["id"], user.pk)
        self.assertEqual(len(res_json["user_photos"]), len(user_photos))
        self.assertEqual(len(res_json["languages"]), len(languages))
        self.assertEqual(len(res_json["user_news"]), len(user_news))
        self.assertEqual(len(res_json["friends"]), len(user_friends))

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

    def test_common_friends(self):
        user1 = UserFactory()
        user2 = UserFactory()
        user_friends = [UserFactory() for _ in range(10)]

        user1.friends.set(user_friends[:7])
        user2.friends.set(user_friends[4:])

        self.client.force_authenticate(user=user1)

        with self.assertNumQueries(8):
            res = self.client.get(self.get_common_friends_url, data={"user": user2.pk})

        res_json = res.json()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res_json["count"], 3)
        self.assertEqual(len(res_json["common_friends"]), len(user_friends[4:7]))

    def test_add_music(self):
        user = UserFactory()
        payload = {
            "user": user.pk,
            # "file": "",
            "title": "Patron",
            "author": "Miyagi",
            # "image": "",
        }

        self.client.force_authenticate(user=user)

        with self.assertNumQueries(1):
            res = self.client.post(self.add_music_url, data=payload)

        res_json = res.json()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Music.objects.count(), 1)

    def test_get_music(self):
        user = UserFactory()
        music = [MusicFactory() for _ in range(10)]

        self.client.force_authenticate(user=user)

        with self.assertNumQueries(1):
            res = self.client.get(self.get_music_url)

        res_json = res.json()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_json), len(music))

    def test_get_user_music(self):
        user = UserFactory()
        music = [MusicFactory() for _ in range(10)]

        user.music.set(music)

        self.client.force_authenticate(user=user)

        with self.assertNumQueries(1):
            res = self.client.get(self.get_user_music_url)

        res_json = res.json()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_json), len(music))

    def test_add_music_to_user(self):
        user = UserFactory()
        music = MusicFactory()

        self.client.force_authenticate(user=user)

        with self.assertNumQueries(2):
            res = self.client.post(f"{self.add_music_to_user_url}?music={music.pk}")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get(id=user.pk).music.count(), 1)

    def test_age_filter(self):
        user1 = UserFactory(age=20)
        user2 = UserFactory(age=19)
        user3 = UserFactory(age=23)

        self.client.force_authenticate(user=user1)

        with self.assertNumQueries(3):
            res = self.client.get(f"{self.list_url}?age_min=18&age_max=25")
            # res = self.client.get(self.list_url, data={"age_min":18, "age_max":25})

            res_json = res.json()
            res_age_list = [user["age"] for user in res_json]
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertTrue(all([user_age > 18 for user_age in res_age_list]))
            self.assertTrue(all([user_age < 25 for user_age in res_age_list]))

    def test_gender_filter(self):
        user1 = UserFactory(gender="Male")
        user2 = UserFactory(gender="Female")
        user3 = UserFactory(gender="Male")

        self.client.force_authenticate(user=user1)

        with self.assertNumQueries(3):
            res = self.client.get(f"{self.list_url}?gender=Male")

        res_json = res.json()
        res_gender_list = [user["gender"] for user in res_json]
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(all([user_gender == "Male" for user_gender in res_gender_list]))

    def test_city_filter(self):
        cities = [CityFactory() for _ in range(3)]
        user1 = UserFactory()
        users = [UserFactory(city=city) for city in cities]

        self.client.force_authenticate(user=user1)

        with self.assertNumQueries(3):
            res = self.client.get(f"{self.list_url}?city={cities[0].slug}")

        res_json = res.json()
        res_city_list = [user["city"] for user in res_json]
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(all([user_city == cities[0].name for user_city in res_city_list]))

    def test_languages_filter(self):
        languages = [LanguageFactory() for _ in range(4)]
        users = [UserFactory() for _ in range(3)]

        for n, user in enumerate(users):
            user.languages.set(languages[n : n + 2])

        self.client.force_authenticate(user=users[0])

        with self.assertNumQueries(3):
            res = self.client.get(f"{self.list_url}?language={languages[1].language_name}")

        res_json = res.json()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_json), 2)
        res_language_list = [
            [lang["language_name"] for lang in user["languages"]] for user in res_json
        ]

        # res_json = [user, user, user, ...]
        # user = {..., ..., "languages": [{"language_name": "eng"}, {"language_name": "rus"}], ..., ..., ...}

        self.assertTrue(
            all(
                [languages[1].language_name in user_language for user_language in res_language_list]
            )
        )
