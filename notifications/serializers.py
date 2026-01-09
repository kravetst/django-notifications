from rest_framework import serializers
from .models import NotificationType, NotificationTemplate

from .validations.html import validate_html
from .validations.variables import validate_variables


class NotificationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationType
        fields = (
            "id",
            "name",
            "channels",
            "variables",
            "is_custom",
        )

    def validate_channels(self, value):
        allowed_channels = {"email", "telegram", "viber", "push"}

        if not value:
            raise serializers.ValidationError(
                "At least one channel must be provided."
            )

        if not set(value).issubset(allowed_channels):
            raise serializers.ValidationError(
                "Invalid channel in channels."
            )

        return value


class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = (
            "id",
            "type",
            "channel",
            "title",
            "html",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")

    def validate(self, attrs):
        channel = attrs.get("channel", self.instance.channel if self.instance else None)
        html = attrs.get("html", self.instance.html if self.instance else None)
        notification_type = attrs.get(
            "type",
            self.instance.type if self.instance else None
        )

        if channel and html:
            validate_html(channel=channel, html=html)

            validate_variables(
                html=html,
                allowed_variables=notification_type.variables,
            )

        return attrs