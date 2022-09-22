init:
	docker exec notify_compose_notify_kafka_pipeline_1 kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 3 --replication-factor 1 --topic email_confirmation
	docker exec notify_compose_notify_kafka_pipeline_1 kafka-topics --create --if-not-exists --zookeeper zookeeper:2181 --partitions 3 --replication-factor 1 --topic password_generation