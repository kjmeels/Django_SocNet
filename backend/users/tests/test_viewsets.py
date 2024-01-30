from functools import partial

from django.urls import reverse
from pytest import mark
from rest_framework import status
from rest_framework.test import APITestCase

from .factories import UserFactory, PhotoFactory


@mark.django_db
class TestUserViewSet(APITestCase):
    def setUp(self):
        self.list_url: str = reverse("users-list")
        self.detail_url = partial(reverse, "users-detail")

    def test_user_list(self):
        users = [UserFactory() for _ in range(5)]
        users_photo = [PhotoFactory(user=user) for user in users for _ in range(5)]

        with self.assertNumQueries(2):
            res = self.client.get(self.list_url)

        res_json = res.json()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_json), len(users))
        self.assertEqual(len(res_json[0]["user_photos"]), len(users_photo) / len(users))

    def test_user_retrieve(self):
        users = [UserFactory() for _ in range(5)]
        users_photo = [PhotoFactory(user=user) for user in users for _ in range(5)]

        with self.assertNumQueries(2):
            res = self.client.get(self.detail_url(kwargs={"pk": users[2].id}))

        res_json = res.json()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res_json["id"], users[2].id)
        self.assertEqual(len(res_json["user_photos"]), len(users_photo) / len(users))
