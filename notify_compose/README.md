![Python](https://img.shields.io/badge/Python-14354C?style=badge&logo=python&logoColor=white)
![Fastapi](https://img.shields.io/badge/Fastapi-000000?style=badge&logo=fastapi&logoColor=white)
![redis](https://img.shields.io/badge/redis-%23DD0031.svg?&style=badge&logo=redis&logoColor=white)
![Kafka](https://img.shields.io/badge/Kafka-FFFFFF?.svg?style=Kafka&logo=kafka)
![Zookeeper](https://img.shields.io/badge/Zookeeper-37F04D?.svg?style=Zookeeper&logo=Zookeeper&logoColor=yellow)
![Clickhouse](https://img.shields.io/badge/Clickhouse-FFFFFF?.svg?style=Clickhouse&logo=Clickhouse&logoColor=yellow)
![Nginx](https://img.shields.io/badge/Nginx-000000?style=badge&logo=nginx&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=badge&logo=docker&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-000000?.svg?style=Gunicorn&logo=Gunicorn&logoColor=green)

# Сервис UGC

Сервис UGC позволяет пользователям оставлять на фильмы лайки, комментарии, добавлять фильмы в закладки, а также
возобновлять просмотр фильма с того момента, на котором пользователь в последний раз остановился.

## Как сервис работает

Kafka - брокер сообщений. Через Kafka данные загружаются в Clickhouse - СУБД для анализа Big Data

Данные в Kafka добавляются через API, написанное на FastAPI

Для использования API необходимо авторизоваться. Для этого необходимо поднять сервис авторизации. Он находится в корне
репозитория в папке auth_service_compose

## Стек технологий

- Python
- FastAPI
- Kafka
- Clickhouse
- Zookeeper
- Nginx
- Docker

# Запуск

Перед запуском необходимо создать _.env_ файлы по примеры _.env.sample_ файлов. Для этого можно воспользоваться скриптом
rename_script.py, который находится в корне репозитория.

Для запуска микросервиса необходимо запустить Docker Compose.

Но перед этим необходимо создать сеть

```
docker network create services_network
```

Перейдите в корень и пропишите команду

```
cd ugc_compose
docker-compose up --build
```

После запуска Docker необходимо создать топики и таблицы. Для этого необходимо запустить Makefile