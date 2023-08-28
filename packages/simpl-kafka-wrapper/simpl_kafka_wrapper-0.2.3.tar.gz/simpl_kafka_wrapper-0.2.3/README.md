
# Repo Setup

Setup aws cli with DE-prod account credentials

```
export CODEARTIFACT_AUTH_TOKEN=`aws codeartifact get-authorization-token --domain simpl --domain-owner 950779425701 --region ap-south-1 --query authorizationToken --output text`                             
poetry config repositories.simpl_utils https://aws:$CODEARTIFACT_AUTH_TOKEN@simpl-950779425701.d.codeartifact.ap-south-1.amazonaws.com/pypi/pypi-store/
poetry config repositories.simpl_kafka_event_publisher https://aws:$CODEARTIFACT_AUTH_TOKEN@simpl-950779425701.d.codeartifact.ap-south-1.amazonaws.com/pypi/pypi-store/
```

### Kafka Config
Below are the available options available for configuring kafka producer behavior

| Attribute                      | Kafka Config Mapping           | Default Value |
|--------------------------------|--------------------------------|---------------|
| `bootstrap_servers`            | `bootstrap.servers`            | Required      |
| `client_id`                    | `client.id`                    | ""            |
| `linger_ms`                    | `linger.ms`                    | `5ms`         |
| `batch_size`                   | `batch.size`                   | `16384`       |
| `delivery_timeout_ms`          | `delivery.timeout.ms`          | `120000`      |
| `batch_num_messages`           | `batch.num.messages`           | `1000`        |
| `compression_type`             | `compression.type`             | `none`        |
| `acks`                         | `acks`                         | `all`         |
| `connections_max_idle_ms`      | `connections.max.idle.ms`      | `540000`      |
| `queue_buffering_max_messages` | `queue.buffering.max.messages` | `100000`      |
| `queue_buffering_max_kbytes`   | `queue.buffering.max.kbytes`   | `100`         |


### Usage

1. Define a KafkaConfig Object
```python
config = KafkaConfig(
    bootstrap_servers="localhost:29092",
    linger_ms=1,
    batch_size=1,
    queue_buffering_max_messages=1,
    batch_num_messages=1
)
```
2. Create a KafkaEventPublisher Object
```python
producer = KafkaEventProducer(config)
```

3. Create an event object schema by inheriting from `BaseEventModel`
```python
class CustomEventModel(BaseEventModel):
    phone_number: str
    user_id: str

...
event = CustomEventModel(phone_number="1234567890", user_id="123")

```

4. Publish messages to kafka using above producer, providing topic name and event
```python
producer.publish("some_topic", event)
````