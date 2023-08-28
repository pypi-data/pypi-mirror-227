import logging
from typing import Literal

from pydantic import BaseModel, ConfigDict

logger = logging.getLogger(__name__)


def to_dot_notation(key: str) -> str:
    return key.replace("_", ".")


class KafkaConfig(BaseModel, validate_assignment=True):
    model_config = ConfigDict(
        alias_generator=to_dot_notation,
        populate_by_name=True,
    )

    # Critical
    bootstrap_servers: str

    # Important
    client_id: str = ""
    linger_ms: int = 5
    batch_size: int = 16384
    delivery_timeout_ms: int = 120000
    batch_num_messages: int = 1000
    compression_type: Literal["none", "gzip", "snappy", "lz4", "zstd"] = "none"
    acks: Literal["0", "1", "all"] = "all"

    # Optional
    connections_max_idle_ms: int = 540000
    queue_buffering_max_messages: int = 100000
    queue_buffering_max_kbytes: int = 100

    # Special

