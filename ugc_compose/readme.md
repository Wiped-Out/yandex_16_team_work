После запуска контейнеров введите команды или запустите Makefile:
```
docker exec ugc_compose_kafka_1 kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 3 --replication-factor 1 --topic user_comments
docker exec ugc_compose_kafka_1 kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 3 --replication-factor 1 --topic film_bookmarks
docker exec ugc_compose_kafka_1 kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 3 --replication-factor 1 --topic film_likes
docker exec ugc_compose_kafka_1 kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 3 --replication-factor 1 --topic film_progress
docker exec clickhouse-node1 clickhouse-client --query="CREATE DATABASE IF NOT EXISTS UGC ON CLUSTER company_cluster;"
docker exec clickhouse-node1 clickhouse-client --query="CREATE TABLE IF NOT EXISTS UGC.film_progress ON CLUSTER company_cluster(user_id UUID,film_id UUID,stamp UInt64) Engine=Kafka SETTINGS kafka_broker_list = 'kafka:9092',kafka_topic_list = 'film_progress', kafka_format = 'JSONEachRow',kafka_group_name = 'group1';"
docker exec clickhouse-node1 clickhouse-client --query="CREATE TABLE IF NOT EXISTS UGC.film_likes ON CLUSTER company_cluster(user_id UUID,film_id UUID) Engine=Kafka SETTINGS kafka_broker_list = 'kafka:9092',kafka_topic_list = 'film_likes',kafka_format = 'JSONEachRow',kafka_group_name = 'group1';"
docker exec clickhouse-node1 clickhouse-client --query="CREATE TABLE IF NOT EXISTS UGC.film_bookmarks ON CLUSTER company_cluster(user_id UUID,film_id UUID) Engine=Kafka SETTINGS kafka_broker_list = 'kafka:9092',kafka_topic_list = 'film_bookmarks',kafka_format = 'JSONEachRow',kafka_group_name = 'group1';"
docker exec clickhouse-node1 clickhouse-client --query="CREATE TABLE IF NOT EXISTS UGC.user_comments  ON CLUSTER company_cluster(user_id UUID,film_id UUID,comment text,created_at UInt64) Engine=Kafka SETTINGS kafka_broker_list = 'kafka:9092',kafka_topic_list = 'user_comments',kafka_format = 'JSONEachRow',kafka_group_name = 'group1';"
```