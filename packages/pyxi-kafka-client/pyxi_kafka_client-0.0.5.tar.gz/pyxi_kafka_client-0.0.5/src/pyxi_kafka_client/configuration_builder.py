from confluent_kafka import Consumer, KafkaError


class ConfigurationBuilder:
    def __init__(self):
        self._config = {}

    def set_bootstrap_servers(self, bootstrap_servers):
        self._config["bootstrap.servers"] = bootstrap_servers
        return self

    def set_group_id(self, group_id: str):
        self._config["group.id"] = group_id
        return self

    def set_offset_reset(self, offset_reset: str):
        self._config["auto.offset.reset"] = offset_reset
        return self

    def build(self) -> dict[str, str]:
        return self._config
