from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from pytest import mark

from notifications.tests.factories import NotificationFactory, NotificationTypeFactory
from users.tests.factories import UserFactory


@mark.django_db
class TestNotificationViewSet(APITestCase):
    def setUp(self):
        self.list_url: str = reverse("notifications-list")

    def test_list(self):
        senders = [UserFactory() for _ in range(4)]
        receivers = [UserFactory() for _ in range(4)]
        type = NotificationTypeFactory()
        notifications = [
            NotificationFactory(
                sender=sender, receiver=receiver, type=type, is_read=[True, False][_ % 2]
            )
            for sender in senders
            for receiver in receivers
            for _ in range(4)
        ]

        for sender in senders:
            sender.friends.set(receivers[:-1])

        self.client.force_authenticate(user=receivers[0])

        with self.assertNumQueries(1):
            res = self.client.get(self.list_url)

        res_json = res.json()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_json), len(notifications) / len(receivers) / 2)
        self.assertEqual(any([x["is_read"] for x in res_json]), False)
