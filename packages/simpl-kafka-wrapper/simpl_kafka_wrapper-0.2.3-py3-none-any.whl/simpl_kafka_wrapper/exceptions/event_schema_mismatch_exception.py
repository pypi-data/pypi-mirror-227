from simpl_kafka_wrapper.exceptions.custom_base_exception import CustomBaseException


class InvalidEventClassException(CustomBaseException):
    def __init__(self, *args, **kwargs) -> None:
        message = f"The schema of event payload does not match the schema of the event class."
        super().__init__(message=message, *args, **kwargs)
