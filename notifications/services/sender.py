from django.template import Template, Context
from django.core.exceptions import ObjectDoesNotExist

from notifications.models import NotificationTemplate
from notifications.services.channels.email import EmailChannel
from notifications.services.channels.push import PushChannel
from notifications.services.channels.telegram import TelegramChannel
from notifications.services.channels.viber import ViberChannel


class NotificationSender:
    """
    High-level service responsible for sending notifications.
    """

    CHANNEL_SERVICES = {
        "email": EmailChannel,
        "telegram": TelegramChannel,
        "viber": ViberChannel,
        "push": PushChannel,
    }

    def send(
        self,
        *,
        notification_type,
        channel: str,
        context: dict,
        recipient: str,
    ):
        """
        Send notification by type and channel.

        :param notification_type: NotificationType instance
        :param channel: 'email' | 'telegram' | 'viber' | 'push'
        :param context: variables for template rendering
        :param recipient: email / chat_id / token
        """

        template = self._get_template(notification_type, channel)
        rendered_html = self._render_template(template.html, context)

        channel_service = self._get_channel_service(channel)

        channel_service.send(
            recipient=recipient,
            title=template.title,
            html=rendered_html,
        )

    def _get_template(self, notification_type, channel):
        try:
            return NotificationTemplate.objects.get(
                type=notification_type,
                channel=channel,
            )
        except ObjectDoesNotExist:
            raise ValueError(
                f"No template for type '{notification_type}' and channel '{channel}'"
            )

    def _render_template(self, html: str, context: dict) -> str:
        template = Template(html)
        return template.render(Context(context))

    def _get_channel_service(self, channel: str):
        service_cls = self.CHANNEL_SERVICES.get(channel)

        if not service_cls:
            raise ValueError(f"Channel '{channel}' is not supported yet")

        return service_cls()