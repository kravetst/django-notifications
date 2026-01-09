from .base import BaseChannel

class TelegramChannel(BaseChannel):
    """
    Заглушка для Telegram.
    """
    def send(self, recipient, title: str, html: str):
        print(f"[Telegram] To: {recipient}, Title: {title}, Message: {html}")
        return True