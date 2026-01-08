from django.db import models
from django.core.exceptions import ValidationError


class NotificationType(models.Model):
    CHANNEL_CHOICES = [
        ("email", "Email"),
        ("telegram", "Telegram"),
        ("viber", "Viber"),
        ("push", "Push"),
    ]

    name = models.CharField(max_length=100, unique=True)
    channels = models.JSONField(default=list)
    variables = models.JSONField(default=list, blank=True)
    is_custom = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def clean(self):
        # Domain-level validation only
        if not self.channels:
            raise ValidationError("Notification type must have at least one channel.")


class NotificationTemplate(models.Model):
    type = models.ForeignKey(
        NotificationType,
        on_delete=models.CASCADE,
        related_name="templates"
    )

    channel = models.CharField(
        max_length=10,
        choices=NotificationType.CHANNEL_CHOICES
    )
    title = models.CharField(max_length=255, blank=True)
    html = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("type", "channel")]

    def __str__(self):
        return f"{self.type.name} - {self.channel}"

    def clean(self):
        # Domain rule: telegram & viber do not support titles
        if self.channel in {"telegram", "viber"} and self.title:
            raise ValidationError(
                {"title": "Title must be empty for telegram and viber."}
            )
