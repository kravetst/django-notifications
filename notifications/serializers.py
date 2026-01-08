from rest_framework import serializers
from .models import NotificationType, NotificationTemplate
import re


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
        channel = attrs.get("channel")
        title = attrs.get("title", "")
        html = attrs.get("html", "")
        notification_type = attrs.get("type")

        # Telegram & Viber must not have title
        if channel in {"telegram", "viber"} and title:
            raise serializers.ValidationError({
                "title": "Title must be empty for telegram and viber."
            })

        # Validate variables usage in html
        if notification_type and notification_type.variables:
            missing_vars = []

            for var in notification_type.variables:
                pattern = r"{{\s*" + re.escape(var) + r"\s*}}"
                if not re.search(pattern, html):
                    missing_vars.append(var)

            if missing_vars:
                raise serializers.ValidationError({
                    "html": f"Missing variables in template: {missing_vars}"
                })

        return attrs