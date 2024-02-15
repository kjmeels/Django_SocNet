from functools import partial

from django.db import IntegrityError
from django.urls import reverse
from pytest import mark
from rest_framework import status
from rest_framework.test import APITestCase

from news.tests.factories import NewsFactory, LikeFactory, CommentFactory, CommentLikeFactory
from .factories import UserFactory
from ..models import News, Like, Comment, CommentLike


@mark.django_db
class TestNewsViewSet(APITestCase):
    def setUp(self):
        self.list_url: str = reverse("news-list")
        self.add_like_url: str = reverse("news-add-like")
        self.destroy_like_url: str = reverse("news-destroy-like")
        self.add_comment_url: str = reverse("news-add-comment")
        self.destroy_comment_url = partial(reverse, "news-destroy-comment")
        self.add_like_to_comment_url: str = reverse("news-add-like-to-comment")
        self.destroy_like_to_comment_url: str = reverse("news-destroy-like-to-comment")

    def test_create(self):
        user = UserFactory()
        payload = {
            "text": "new news",
            "image": "",
        }

        with self.assertNumQueries(0):
            res = self.client.post(self.list_url, data=payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=user)

        with self.assertNumQueries(1):
            res = self.client.post(self.list_url, data=payload)

        res_json = res.json()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
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

    def test_add_comment(self):
        user = UserFactory()
        new = NewsFactory()
        payload = {
            "new": new.pk,
            "text": "comment text",
        }

        self.client.force_authenticate(user=user)

        with self.assertNumQueries(2):
            res = self.client.post(self.add_comment_url, data=payload)

        res_json = res.json()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_json["new"], new.pk)
        self.assertEqual(Comment.objects.count(), 1)

    def test_destroy_comment(self):
        user = UserFactory()
        new = NewsFactory()
        comment = CommentFactory(user=user, new=new)

        self.client.force_authenticate(user=user)

        with self.assertNumQueries(3):
            res = self.client.delete(self.destroy_comment_url(kwargs={"pk": comment.id}))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

    def test_add_comment_like(self):
        user = UserFactory()
        new = NewsFactory()
        comment = CommentFactory(user=user, new=new)
        payload = {
            "comment": comment.pk,
            "text": "comment text",
        }

        self.client.force_authenticate(user=user)

        with self.assertNumQueries(2):
            res = self.client.post(self.add_like_to_comment_url, data=payload)

        res_json = res.json()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_json["comment"], comment.pk)
        self.assertEqual(CommentLike.objects.count(), 1)

        try:
            with self.assertNumQueries(2):
                res = self.client.post(self.add_like_to_comment_url, data={"comment": comment.pk})
            self.fail("Не отработал UniqueConstraint")
        except IntegrityError:
            pass
        except Exception:
            self.fail("Не отработал UniqueConstraint")

    def test_destroy_comment_like(self):
        user = UserFactory()
        new = NewsFactory()
        comment = CommentFactory(user=user, new=new)
        comment_like = CommentLikeFactory(user=user, comment=comment)

        self.client.force_authenticate(user=user)

        with self.assertNumQueries(2):
            res = self.client.delete(f"{self.destroy_like_to_comment_url}?comment={comment.pk}")

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CommentLike.objects.count(), 0)
