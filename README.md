# Описание
Django проект, который позволяет пользователям создавать, читать, обновлять и удалять песни, альбомы и исполнителей. Проект использует django-rest-framework для создания RESTful API для управления данными.

# Стек технологий:

----------
* Python 3.11
* Django 4.1
* django-rest-framework 3.14
* PostgreSQL

# Запуск проекта в контейнерах

- Клонирование удаленного репозитория
```bash
git clone git@github.com:ArtKeyplex/music_catalog_api.git
```
- Сборка и развертывание контейнеров
```bash
docker-compose up -d --build
```
- Выполните миграции
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

Зайдите в проект по адресу http://localhost:8000/swagger/. Вы увидите swagger с полным описанием API.
