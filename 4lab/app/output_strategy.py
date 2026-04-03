import configparser
import json
import os
import time
from abc import ABC, abstractmethod


class OutputStrategy(ABC):
    @abstractmethod
    def write(self, records):
        raise NotImplementedError()


class ConsoleStrategy(OutputStrategy):
    def write(self, records):
        for record in records:
            print(json.dumps(record, ensure_ascii=False))


class FileStrategy(OutputStrategy):
    def __init__(self, path):
        self.path = path

    def write(self, records):
        with open(self.path, "w", encoding="utf-8") as stream:
            json.dump(records, stream, indent=2, ensure_ascii=False)
        print(f"Saved {len(records)} records to file '{self.path}'")


class RedisStrategy(OutputStrategy):
    def __init__(self, url, key):
        try:
            import redis
        except ImportError as exc:
            raise RuntimeError(
                "Redis strategy requires the 'redis' package. Install it in requirements.txt."
            ) from exc

        self.url = url
        self.key = key
        self.client = self._connect()

    def _connect(self):
        import redis

        for attempt in range(5):
            try:
                client = redis.from_url(self.url, decode_responses=True)
                client.ping()
                return client
            except Exception:
                time.sleep(2)
        raise RuntimeError(f"Unable to connect to Redis at {self.url}")

    def write(self, records):
        payload = json.dumps(records, ensure_ascii=False)
        self.client.set(self.key, payload)
        print(f"Saved {len(records)} records to Redis key '{self.key}'")


class KafkaStrategy(OutputStrategy):
    def __init__(self, bootstrap_servers, topic):
        try:
            from kafka import KafkaProducer
        except ImportError as exc:
            raise RuntimeError(
                "Kafka strategy requires the 'kafka-python' package. Install it in requirements.txt."
            ) from exc

        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
        self.producer = self._connect(KafkaProducer)

    def _connect(self, producer_cls):
        for attempt in range(5):
            try:
                return producer_cls(
                    bootstrap_servers=self.bootstrap_servers,
                    value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode("utf-8"),
                )
            except Exception:
                time.sleep(2)
        raise RuntimeError(f"Unable to connect to Kafka at {self.bootstrap_servers}")

    def write(self, records):
        for record in records:
            self.producer.send(self.topic, record)
        self.producer.flush()
        print(f"Published {len(records)} records to Kafka topic '{self.topic}'")


def load_json_config(path):
    with open(path, "r", encoding="utf-8") as stream:
        return json.load(stream)


def load_ini_config(path):
    parser = configparser.ConfigParser()
    parser.read(path, encoding="utf-8")
    config = {}

    if parser.has_section("output"):
        config["output_strategy"] = parser.get("output", "strategy", fallback=None)
        file_path = parser.get("output", "file_path", fallback=None)
        if file_path:
            config["file"] = {"path": file_path}

    if parser.has_section("redis"):
        config["redis"] = {
            "url": parser.get("redis", "url", fallback=None),
            "key": parser.get("redis", "key", fallback=None),
        }

    if parser.has_section("kafka"):
        config["kafka"] = {
            "bootstrap_servers": parser.get("kafka", "bootstrap_servers", fallback=None),
            "topic": parser.get("kafka", "topic", fallback=None),
        }

    return config


def load_config(path=None):
    config_path = path or os.environ.get("OUTPUT_CONFIG_PATH")
    if config_path:
        config_path = str(config_path)
    else:
        if os.path.exists("config.ini"):
            config_path = "config.ini"
        elif os.path.exists("config.json"):
            config_path = "config.json"
        else:
            return {}

    if not os.path.exists(config_path):
        return {}

    if config_path.lower().endswith(".ini"):
        return load_ini_config(config_path)

    return load_json_config(config_path)


def build_strategy(config_path=None):
    config = load_config(config_path)
    strategy_name = os.environ.get(
        "OUTPUT_STRATEGY",
        config.get("output_strategy", "console"),
    ).lower()

    if strategy_name == "console":
        return ConsoleStrategy()
    if strategy_name == "file":
        file_config = config.get("file", {})
        return FileStrategy(
            file_config.get("path", os.environ.get("OUTPUT_FILE_PATH", "output_records.json"))
        )
    if strategy_name == "redis":
        redis_config = config.get("redis", {})
        return RedisStrategy(
            redis_config.get("url", os.environ.get("REDIS_URL", "redis://redis:6379")),
            redis_config.get("key", os.environ.get("REDIS_KEY", "parking_records")),
        )
    if strategy_name == "kafka":
        kafka_config = config.get("kafka", {})
        return KafkaStrategy(
            kafka_config.get(
                "bootstrap_servers", os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
            ),
            kafka_config.get("topic", os.environ.get("KAFKA_TOPIC", "parking_violations")),
        )

    raise ValueError(f"Unknown output strategy: {strategy_name}")
