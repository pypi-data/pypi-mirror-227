from typing import Optional
from confluent_kafka import Consumer, KafkaError
from .configuration_builder import ConfigurationBuilder
from .secret_provider import SecretProvider


class KafkaConsumerManager:
    def __init__(self, topic: str, consumer_group_id: str):
        self._secret_provider = SecretProvider()
        self._topic = topic
        self._consumer_group_id = consumer_group_id

    def init(self, configuration: Optional[dict[str, str]] = None):
        self._configuration = (
            ConfigurationBuilder(configuration)
            .set_group_id(self._consumer_group_id)
            .set_offset_reset("earliest")
        ).build()

        # self._configuration = self._configuration_builder.set_bootstrap_servers(
        #     self._secret_provider.get_secret("BOOTSTRAP_SERVER")
        # ).build()

        self._consumer = Consumer(self._configuration)
        return self

    def subscribe(self):
        self._consumer.subscribe([self._topic])
        return self

    def poll(self, timeout: Optional[int] = 1):
        return self._consumer.poll(timeout)

    def manage(self):
        try:
            while True:
                msg = self._consumer.poll(1.0)
                if msg is None:
                    print("no message received by consumer")
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        print("End of partition reached")
                    else:
                        print(f"Error: {msg.error()}")
                else:
                    print(f"Received message: {msg.value().decode('utf-8')}")
        except KeyboardInterrupt:
            self.dispose()

    def dispose(self):
        self._consumer.close()
        return self
