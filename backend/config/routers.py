from rest_framework.routers import DefaultRouter

from news.viewsets import NewsViewSet
from notifications.viewsets import NotificationViewSet
from users.viewsets import UserViewSet

router = DefaultRouter()


router.register(r"users", UserViewSet, basename="users")
router.register(r"news", NewsViewSet, basename="news")
router.register(r"notifications", NotificationViewSet, basename="notifications")
