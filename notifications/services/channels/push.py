from .base import BaseChannel

class PushChannel(BaseChannel):
    """
    Заглушка для Push notification.
    """
    def send(self, recipient, title: str, html: str):
        print(f"[Push] To: {recipient}, Title: {title}, Message: {html}")
        return True
