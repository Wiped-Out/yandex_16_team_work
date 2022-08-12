После запуска контейнеров введите комманды:
```
docker exec ugc_compose_kafka_1 kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 3 --replication-factor 1 --topic user_comments
docker exec ugc_compose_kafka_1 kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 3 --replication-factor 1 --topic film_bookmarks
docker exec ugc_compose_kafka_1 kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 3 --replication-factor 1 --topic film_likes
docker exec ugc_compose_kafka_1 kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 3 --replication-factor 1 --topic film_progress

```