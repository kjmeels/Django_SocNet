from django.apps import AppConfig


class NewsConfig(AppConfig):
    name: str = "news"
    verbose_name: str = "Новости"

    def ready(self):
        from . import signals
