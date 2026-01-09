from django.core.mail import send_mail
from .base import BaseChannel

class EmailChannel(BaseChannel):
    """
    Implementing the Email channel.
    """

    def send(self, recipient, title: str, html: str):
        """
        Uses Django send_mail for sending.
        """
        send_mail(
            subject=title,
            message='',  # can be left blank
            html_message=html,
            from_email=None,  # using DEFAULT_FROM_EMAIL from settings
            recipient_list=[recipient],
            fail_silently=False,
        )
        return True