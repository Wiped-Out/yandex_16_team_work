from kafka import KafkaProducer
from core.config import settings

producer = KafkaProducer(bootstrap_servers=[f"{settings.KAFKA_HOST}:{settings.KAFKA_PORT}"])
