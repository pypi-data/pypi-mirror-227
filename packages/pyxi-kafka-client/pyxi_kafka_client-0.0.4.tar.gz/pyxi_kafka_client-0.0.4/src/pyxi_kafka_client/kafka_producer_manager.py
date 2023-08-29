from confluent_kafka import Consumer, Producer, KafkaError
from .configuration_builder import ConfigurationBuilder
from .secret_provider import SecretProvider
from typing import Optional


class KafkaProducerManager:
    def __init__(self, topic: str):
        self._configuration_builder = ConfigurationBuilder()
        self._secret_provider = SecretProvider()
        self._topic = topic

    def init(self, configuration: Optional[dict[str, str]] = None):
        if configuration is not None:
            self._configuration = configuration
        else:
            self._configuration = self._configuration_builder.set_bootstrap_servers(
                self._secret_provider.get_secret("BOOTSTRAP_SERVER")
            ).build()

        self._producer = Producer(self._configuration)
        return self

    def produce(self, key: str, value: str):
        self._producer.produce(self._topic, key=key, value=value)
        return self

    # Wait for any outstanding messages to be delivered and delivery reports received
    def flush(self):
        self._producer.flush()
        return self
