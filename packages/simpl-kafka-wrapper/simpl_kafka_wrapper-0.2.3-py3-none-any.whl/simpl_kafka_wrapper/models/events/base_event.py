import re
from uuid import uuid4, UUID
from datetime import datetime
from typing import ClassVar

import pytz
from pydantic import BaseModel, field_validator, Field, ConfigDict


class BaseEventModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    event_id: str = Field(default_factory=lambda: str(uuid4()))
    event_timestamp: str = datetime.now(pytz.timezone("Asia/Kolkata")).isoformat(timespec="milliseconds")
    event_type: str
    version: str

    MIN_EVENT_NAME_LENGTH: ClassVar = 5

    @field_validator("event_id", mode="before")
    def event_id_must_be_valid_uuid(cls, value: str) -> str:
        if value is None or value == "":
            return str(uuid4())
        try:
            UUID(value)
        except ValueError:
            raise ValueError("Invalid Event ID. It should be a valid UUIDv4")
        return value

    @field_validator("event_type")
    def event_type_must_be_valid(cls, value: str) -> str:
        if value is None or not isinstance(value, str):
            raise ValueError("Invalid Event Type. It should be a valid string")
        if len(value) < cls.MIN_EVENT_NAME_LENGTH:
            raise ValueError(
                "Invalid Event Type. String Length should be at least {}".format(cls.MIN_EVENT_NAME_LENGTH))
        return value

    @field_validator("version")
    def version_must_be_valid(cls, value: str) -> str:
        if value is None or not isinstance(value, str):
            raise ValueError("Invalid Version. It should be a valid string")
        if re.compile(r"[0-9]+(\.[0-9]+)*").match(value) is None:
            raise ValueError("Invalid Version. It should be a valid semantic version like 1.23.3")
        return value
