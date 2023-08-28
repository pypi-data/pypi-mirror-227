from confluent_kafka import KafkaException


class CustomBaseException(Exception):
    """Base custom exception for my application."""

    def __init__(self, *args, **kwargs):
        self.message = kwargs.pop("message")
        self.kwargs = kwargs
        super().__init__(*args)

    def __str__(self) -> str:
        return self.message or f'{self.__class__.__name__} was raised'

    def __repr__(self) -> str:
        if self.message is None or self.message == '':
            return f'{self.__class__.__name__} was raised.'
        return f'{self.__class__.__name__}({self.message!r})'

    def to_dict(self) -> dict:
        """Convert the exception to a dictionary representation."""
        return {
            'class': self.__class__.__name__,
            'message': self.message,
            **self.kwargs,
        }


class CustomKafkaException(KafkaException):
    def __init__(self, *args, **kwargs):
        self.message = kwargs.pop("message")
        self.kwargs = kwargs
        super().__init__(*args)

    def __str__(self) -> str:
        return self.message or f'{self.__class__.__name__} was raised'

    def __repr__(self) -> str:
        if self.message is None or self.message == '':
            return f'{self.__class__.__name__} was raised.'
        return f'{self.__class__.__name__}({self.message!r})'

    def to_dict(self) -> dict:
        """Convert the exception to a dictionary representation."""
        return {
            'class': self.__class__.__name__,
            'message': self.message,
            **self.kwargs,
        }
