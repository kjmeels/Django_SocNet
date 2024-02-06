from rest_framework.routers import DefaultRouter

from news.viewsets import NewsViewSet
from users.viewsets import UserViewSet

router = DefaultRouter()


router.register(r"users", UserViewSet, basename="users")
router.register(r"news", NewsViewSet, basename="news")
