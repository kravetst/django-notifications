from abc import ABC, abstractmethod


class BaseChannel(ABC):
    """
    Abstract class for distribution channels.
    Each channel must implement the send() method.
    """

    @abstractmethod
    def send(self, recipient, title: str, html: str):
        """
        Sends a message to a specific user.
        :param recipient: recipient (email, telegram id, viber id, push token)
        :param title: message title (for email, push)
        :param html: message content
        """
        pass