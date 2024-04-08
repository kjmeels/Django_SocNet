# My social network

Социальная сеть с возможностью ведения личного блога (страницы), оцениванием постов (лайками),
расширением сети друзей и просмотром новостей людей, на которых подписаны. 
Также реализовал рассылку уведомлений подписчикам при создании новости и при получении лайка.

## ENVs:
```
SITE_HOST=localhost
SECRET_KEY=my_secret_key
DEBUG=True
POSTGRES_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_PORT=5432
```

## Third party packages:
```
rest_framework
drf_spectacular
django_filters
solo
ckeditor
adminsortable2
colorful
```

### Локальный запуск проекта 
```shell
docker compose build
docker compose up
```

| Доступ  | Ссылка                        |
|---------|-------------------------------|
| Админка | http://0.0.0.0:8000/admin/    |
| Сваггер | http://0.0.0.0:8000/api/docs/ |


