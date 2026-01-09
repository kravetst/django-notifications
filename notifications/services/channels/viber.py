from .base import BaseChannel

class ViberChannel(BaseChannel):
    """
    Заглушка для Viber.
    """
    def send(self, recipient, title: str, html: str):
        print(f"[Viber] To: {recipient}, Title: {title}, Message: {html}")
        return True