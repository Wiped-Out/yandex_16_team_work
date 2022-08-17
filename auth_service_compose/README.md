![Python](https://img.shields.io/badge/Python-14354C?style=badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-FFFFFF?style=badge&logo=flask&logoColor=black)
![redis](https://img.shields.io/badge/redis-%23DD0031.svg?&style=badge&logo=redis&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=badge&logo=postgresql&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-000000?style=badge&logo=nginx&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=badge&logo=docker&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-000000?.svg?style=Gunicorn&logo=Gunicorn&logoColor=green)

# Сервис авторизации

Сервис авторизации позволяет авторизоваться с помощью технологий JWT или OAuth от Google (мы предусмотрели возможность
добавления OAuth сервисом от других компаний, например, от Яндекса или VK)

## Как сервис работает

### Регистрация

Пользователь регистрируется в системе через форму регистрации либо через OAuth сервис. При регистрации через Oauth
сервис генерируем пользователю пароль и запоминаем, что пользователь использует для авторизации OAuth

### Токены авторизации

Используем **auth** и **refresh** токены.

Время жизни **auth** токена - 2 минуты. При истечении времени жизни будет использован refresh токен для генерации нового
auth токена.

Время жизни **refresh** токена - 30 дней. При истечении времени жизни сервис попросит залогиниться снова, а **refresh**
токен будет сохранен в Redis как невалидный.

Также если потребуется отобрать доступ, можно положить **refresh** токен в Redis, не дожидаясь окончания срока
действия **refresh** токена

## Стек технологий

- Python
- Flask
- JWT
- OAuth
- Redis
- PostgreSQL
- Nginx
- Docker

# Запуск

Перед запуском необходимо создать _.env_ файлы по примеры _.env.sample_ файлов. Для этого можно воспользоваться скриптом
rename_script.py, который находится в корне репозитория.

Для запуска микросервиса необходимо запустить Docker Compose.
Перейдите в корень и пропишите команду

```
cd auth_service_compose
docker-compose up --build
```