![Kibana](https://img.shields.io/badge/kibana-000000?style=badge&logo=kibana)
![Logstash](https://img.shields.io/badge/logstash-321321?style=badge&logo=logstash)
![Elasticsearch](https://img.shields.io/badge/elasticsearch-123123?style=badge&logo=elasticsearch)

# Сервис ELK

Сервис ELK для просмотра логов из других сервисов.

## Как сервис работает

Другие сервисы, если включена отправка логов в logstash, отправляют логи в Logstash.

Logstash сохраняет логи в датированные одноименные с тегами индексы в Elasticsearch

Посредством создания паттернов индексов в Kibana можно просматривать статистику логов и не только

## Стек технологий

- Kibana
- Logstash
- Elasticsearch

# Запуск

Данный сервис следует запускать первым, если включена отправка логов

Перед запуском необходимо создать _.env_ файлы по примеры _.env.sample_ файлов. Для этого можно воспользоваться скриптом
rename_script.py, который находится в корне репозитория.

Для запуска микросервиса необходимо запустить Docker Compose. Перейдите в корень и пропишите команду

```
cd elk_compose
docker-compose up --build
```