init:
	docker exec ugc_compose_kafka_1 kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 3 --replication-factor 1 --topic user_comments
	docker exec ugc_compose_kafka_1 kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 3 --replication-factor 1 --topic film_bookmarks
	docker exec ugc_compose_kafka_1 kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 3 --replication-factor 1 --topic film_likes
	docker exec ugc_compose_kafka_1 kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 3 --replication-factor 1 --topic film_progress
	docker exec clickhouse-node1 clickhouse-client --query="CREATE DATABASE IF NOT EXISTS from_Kafka;"

	docker exec clickhouse-node1 clickhouse-client --query="CREATE TABLE IF NOT EXISTS from_Kafka.film_progress(user_id UUID,film_id UUID,stamp UInt64) Engine=Kafka SETTINGS kafka_broker_list = 'kafka:9092',kafka_topic_list = 'film_progress', kafka_format = 'JSONEachRow',kafka_group_name = 'group1';"
	docker exec clickhouse-node1 clickhouse-client --query="CREATE TABLE IF NOT EXISTS from_Kafka.film_likes(user_id UUID,film_id UUID) Engine=Kafka SETTINGS kafka_broker_list = 'kafka:9092',kafka_topic_list = 'film_likes',kafka_format = 'JSONEachRow',kafka_group_name = 'group1';"
	docker exec clickhouse-node1 clickhouse-client --query="CREATE TABLE IF NOT EXISTS from_Kafka.film_bookmarks(user_id UUID,film_id UUID) Engine=Kafka SETTINGS kafka_broker_list = 'kafka:9092',kafka_topic_list = 'film_bookmarks',kafka_format = 'JSONEachRow',kafka_group_name = 'group1';"
	docker exec clickhouse-node1 clickhouse-client --query="CREATE TABLE IF NOT EXISTS from_Kafka.user_comments(user_id UUID,film_id UUID,comment text,created_at UInt64) Engine=Kafka SETTINGS kafka_broker_list = 'kafka:9092',kafka_topic_list = 'user_comments',kafka_format = 'JSONEachRow',kafka_group_name = 'group1';"

	docker exec clickhouse-node1 clickhouse-client --query="CREATE DATABASE IF NOT EXISTS shard;"
	docker exec clickhouse-node1 clickhouse-client --query="CREATE DATABASE IF NOT EXISTS replica;"

	docker exec clickhouse-node1 clickhouse-client --query="CREATE TABLE IF NOT EXISTS shard.film_progress(user_id UUID,film_id UUID,stamp UInt64) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/film_progress', 'film_progress_replica_1') ORDER by user_id"
	docker exec clickhouse-node1 clickhouse-client --query="CREATE TABLE IF NOT EXISTS replica.film_progress(user_id UUID,film_id UUID,stamp UInt64) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/film_progress', 'film_progress_replica_2') ORDER by user_id"

	docker exec clickhouse-node1 clickhouse-client --query="CREATE TABLE IF NOT EXISTS shard.film_likes(user_id UUID,film_id UUID) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/film_likes', 'film_likes_replica_1') ORDER by user_id"
	docker exec clickhouse-node1 clickhouse-client --query="CREATE TABLE IF NOT EXISTS replica.film_likes(user_id UUID,film_id UUID) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/film_likes', 'film_likes_replica_2') ORDER by user_id"

	docker exec clickhouse-node1 clickhouse-client --query="CREATE TABLE IF NOT EXISTS shard.film_bookmarks(user_id UUID,film_id UUID) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/film_bookmarks', 'film_bookmarks_replica_1') ORDER by user_id"
	docker exec clickhouse-node1 clickhouse-client --query="CREATE TABLE IF NOT EXISTS replica.film_bookmarks(user_id UUID,film_id UUID) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/film_bookmarks', 'film_bookmarks_replica_2') ORDER by user_id"

	docker exec clickhouse-node1 clickhouse-client --query="CREATE TABLE IF NOT EXISTS shard.user_comments(user_id UUID,film_id UUID,comment text,created_at UInt64) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/user_comments', 'user_comments_replica_1') ORDER by user_id"
	docker exec clickhouse-node1 clickhouse-client --query="CREATE TABLE IF NOT EXISTS replica.user_comments(user_id UUID,film_id UUID,comment text,created_at UInt64) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/user_comments', 'user_comments_replica_2') ORDER by user_id"

	docker exec clickhouse-node1 clickhouse-client --query="CREATE TABLE IF NOT EXISTS default.film_progress (user_id UUID,film_id UUID,stamp UInt64) ENGINE = Distributed('company_cluster', '', film_progress, rand());"
	docker exec clickhouse-node1 clickhouse-client --query="CREATE TABLE IF NOT EXISTS default.film_likes (user_id UUID,film_id UUID) ENGINE = Distributed('company_cluster', '', film_likes, rand());"
	docker exec clickhouse-node1 clickhouse-client --query="CREATE TABLE IF NOT EXISTS default.film_bookmarks (user_id UUID,film_id UUID) ENGINE = Distributed('company_cluster', '', film_bookmarks, rand());"
	docker exec clickhouse-node1 clickhouse-client --query="CREATE TABLE IF NOT EXISTS default.user_comments (user_id UUID,film_id UUID,comment text,created_at UInt64) ENGINE = Distributed('company_cluster', '', user_comments, rand());"

	docker exec clickhouse-node1 clickhouse-client --query="CREATE MATERIALIZED VIEW IF NOT EXISTS default.film_progress_consumer TO default.film_progress AS SELECT * FROM from_Kafka.film_progress;"
	docker exec clickhouse-node1 clickhouse-client --query="CREATE MATERIALIZED VIEW IF NOT EXISTS default.film_likes_consumer TO default.film_likes AS SELECT * FROM from_Kafka.film_likes;"
	docker exec clickhouse-node1 clickhouse-client --query="CREATE MATERIALIZED VIEW IF NOT EXISTS default.film_bookmarks_consumer TO default.film_bookmarks AS SELECT * FROM from_Kafka.film_bookmarks;"
	docker exec clickhouse-node1 clickhouse-client --query="CREATE MATERIALIZED VIEW IF NOT EXISTS default.user_comments_consumer TO default.user_comments AS SELECT * FROM from_Kafka.user_comments;"

	docker exec clickhouse-node3 clickhouse-client --query="CREATE DATABASE IF NOT EXISTS shard;"
	docker exec clickhouse-node3 clickhouse-client --query="CREATE DATABASE IF NOT EXISTS replica;"

	docker exec clickhouse-node3 clickhouse-client --query="CREATE TABLE IF NOT EXISTS shard.film_progress(user_id UUID,film_id UUID,stamp UInt64) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/film_progress', 'film_progress_replica_1') ORDER by user_id"
	docker exec clickhouse-node3 clickhouse-client --query="CREATE TABLE IF NOT EXISTS replica.film_progress(user_id UUID,film_id UUID,stamp UInt64) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/film_progress', 'film_progress_replica_2') ORDER by user_id"

	docker exec clickhouse-node3 clickhouse-client --query="CREATE TABLE IF NOT EXISTS shard.film_likes(user_id UUID,film_id UUID) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/film_likes', 'film_likes_replica_1') ORDER by user_id"
	docker exec clickhouse-node3 clickhouse-client --query="CREATE TABLE IF NOT EXISTS replica.film_likes(user_id UUID,film_id UUID) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/film_likes', 'film_likes_replica_2') ORDER by user_id"

	docker exec clickhouse-node3 clickhouse-client --query="CREATE TABLE IF NOT EXISTS shard.film_bookmarks(user_id UUID,film_id UUID) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/film_bookmarks', 'film_bookmarks_replica_1') ORDER by user_id"
	docker exec clickhouse-node3 clickhouse-client --query="CREATE TABLE IF NOT EXISTS replica.film_bookmarks(user_id UUID,film_id UUID) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/film_bookmarks', 'film_bookmarks_replica_2') ORDER by user_id"

	docker exec clickhouse-node3 clickhouse-client --query="CREATE TABLE IF NOT EXISTS shard.user_comments(user_id UUID,film_id UUID,comment text,created_at UInt64) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/user_comments', 'user_comments_replica_1') ORDER by user_id"
	docker exec clickhouse-node3 clickhouse-client --query="CREATE TABLE IF NOT EXISTS replica.user_comments(user_id UUID,film_id UUID,comment text,created_at UInt64) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/user_comments', 'user_comments_replica_2') ORDER by user_id"

	docker exec clickhouse-node3 clickhouse-client --query="CREATE TABLE IF NOT EXISTS default.film_progress (user_id UUID,film_id UUID,stamp UInt64) ENGINE = Distributed('company_cluster', '', film_progress, rand());"
	docker exec clickhouse-node3 clickhouse-client --query="CREATE TABLE IF NOT EXISTS default.film_likes (user_id UUID,film_id UUID) ENGINE = Distributed('company_cluster', '', film_likes, rand());"
	docker exec clickhouse-node3 clickhouse-client --query="CREATE TABLE IF NOT EXISTS default.film_bookmarks (user_id UUID,film_id UUID) ENGINE = Distributed('company_cluster', '', film_bookmarks, rand());"
	docker exec clickhouse-node3 clickhouse-client --query="CREATE TABLE IF NOT EXISTS default.user_comments (user_id UUID,film_id UUID,comment text,created_at UInt64) ENGINE = Distributed('company_cluster', '', user_comments, rand());"
