from simpl_kafka_wrapper.exceptions.custom_base_exception import CustomBaseException
from simpl_kafka_wrapper.models.events import BaseEventModel


class InvalidEventClassException(CustomBaseException):
    def __init__(self, *args, **kwargs) -> None:
        message = f"Instance should be an instance of/child of {BaseEventModel.__class__} class."
        super().__init__(message=message, *args, **kwargs)
