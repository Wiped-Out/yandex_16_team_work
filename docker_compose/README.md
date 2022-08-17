![Python](https://img.shields.io/badge/Python-14354C?style=badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=badge&logo=django&logoColor=white)
![Fastapi](https://img.shields.io/badge/Fastapi-000000?style=badge&logo=fastapi&logoColor=white)
![redis](https://img.shields.io/badge/redis-%23DD0031.svg?&style=badge&logo=redis&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=badge&logo=postgresql&logoColor=white)
![Elasticsearch](https://badges.aleen42.com/src/elasticsearch.svg)
![Nginx](https://img.shields.io/badge/Nginx-000000?style=badge&logo=nginx&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=badge&logo=docker&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-000000?.svg?style=Gunicorn&logo=Gunicorn&logoColor=green)

# Сервис Admin Panel и сервис Async API

Сервис Admin Panel позволяет менеджерам добавлять/удалять/изменять информацию о фильмах, жанрах и актёрах

Сервис Async API позволяет получать информацию о фильмах, жанрах и актерах

Информация из Admin Panel постоянно загружается в сервис Async API через ETL

## Как сервисы работают

Сервис Admin Panel написан на Django. Менеджер входит в аккаунт. После он может редактировать данные в базе данных
PostgreSQL

Каждые 10 минут данные из PostgreSQL загружаются в Elasticsearch (сервис Async API)

Для запросов в Async API необходимо авторизоваться через сервис авторизации (docker compose сервиса находится в корне
проекта)

API позволяет искать фильмы и актеров с помощью эндпоинта /search. Также можно получать все фильмы, всех актеров и все
жанры. У сервиса есть документация в OpenAPI

## Стек технологий

- Python
- Django
- FastAPI
- Redis
- PostgreSQL
- Elasticsearch
- Nginx
- Docker

# Запуск

Перед запуском необходимо создать _.env_ файлы по примеры _.env.sample_ файлов. Для этого можно воспользоваться скриптом
rename_script.py, который находится в корне репозитория.

Для запуска микросервиса необходимо запустить Docker Compose.
Перейдите в корень и пропишите команду

```
cd docker-compose
docker-compose up --build
```

После необходимо создать индексы в Elasticsearch. Для этого запустите файл Makefile, находящийся там же, где и
docker-compose.yaml