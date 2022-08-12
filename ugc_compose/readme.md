После запуска контейнеров введите комманды:
```
docker exec ugc_compose_kafka_1 kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 3 --replication-factor 1 --topic comments
docker exec ugc_compose_kafka_1 kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 3 --replication-factor 1 --topic bookmarks
docker exec ugc_compose_kafka_1 kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 3 --replication-factor 1 --topic likes
docker exec ugc_compose_kafka_1 kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 3 --replication-factor 1 --topic film_progress

```