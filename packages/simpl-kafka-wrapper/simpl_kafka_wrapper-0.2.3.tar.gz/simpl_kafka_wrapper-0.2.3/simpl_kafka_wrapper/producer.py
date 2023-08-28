import json
from threading import Thread

from confluent_kafka import KafkaError, Producer
from confluent_kafka import Message as KafkaMessage

from simpl_kafka_wrapper.exceptions.custom_base_exception import CustomKafkaException
from simpl_kafka_wrapper.exceptions.invalid_event_class_exception import InvalidEventClassException
from simpl_kafka_wrapper.models.configs.kafka.kafka_config import KafkaConfig
from simpl_kafka_wrapper.models.events import BaseEventModel
from simpl_kafka_wrapper.utils import Singleton


class KafkaEventProducer(metaclass=Singleton):
    def __init__(self, kafka_config: KafkaConfig):
        """
        Custom Kafka Producer to publish the events to the Kafka Instance. It is a singleton class. This publisher
        requires a KafkaConfig object to be passed to it. The KafkaConfig object contains the configuration for the \
        producer.
        :param kafka_config: type: KafkaConfig
        """
        # Model Dump by alias is used to convert the model to a dict with the alias names
        # So field linger_ms is converted to linger.ms in the dict key
        self._producer = Producer(kafka_config.model_dump(by_alias=True))
        self._cancelled = False
        self._poll_thread = Thread(target=self.poll_loop)
        self._poll_thread.start()

    def poll_loop(self) -> None:
        while not self._cancelled:
            self._producer.poll(0.1)

    def close(self) -> None:
        self._cancelled = True
        self._producer.flush()
        self._poll_thread.join()

    def flush(self, **kwargs) -> None:
        self._producer.flush(**kwargs)

    def _check_kafka_connection(self) -> None:
        if self._producer is not None:
            self._producer.list_topics(timeout=5)

    @staticmethod
    def acknowledgment(error: KafkaError, message: KafkaMessage):
        if error:
            # In case of an exception, the future is set as exception and the airbrake is notified.
            raise CustomKafkaException(message=message.error().str(), topic=message.topic())

    def produce(self, topic: str, event: BaseEventModel, callback=None) -> bool:
        """
        Publishes the event payload to the particular Topic on the defined Kafka Instance.
        :param topic: The topic to which the message needs to be published.
        :param event: The event payload to be published. It should be a subclass of BaseEventModel
        :param callback: You can provide a custom callback function to be called when the message is delivered. If not \
        provided, the default acknowledgment function is called.
        :return: True if the message is published successfully, False otherwise.
        """
        if not isinstance(event, BaseEventModel):
            raise InvalidEventClassException()

        _event = json.dumps(event.model_dump(), default=str).encode("utf-8")

        try:
            self._producer.produce(topic, _event, on_delivery=callback or self.acknowledgment)
        except BufferError:
            # Putting the poll() first to block until there is queue space available.
            # Waiting for 5 seconds and retrying
            self._producer.poll(5)
            self._producer.produce(
                topic, _event, on_delivery=self.acknowledgment
            )
            return False
        return True

