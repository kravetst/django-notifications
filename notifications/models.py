from django.db import models
from django.core.exceptions import ValidationError


class NotificationType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    # Distribution Channels
    CHANNEL_CHOICES = [
        ("email", "Email"),
        ("telegram", "Telegram"),
        ("viber", "Viber"),
        ("push", "Push"),
    ]
    channels = models.JSONField(default=list)
    variables = models.JSONField(default=list, blank=True)

    # Is this a custom type added by the superuser
    is_custom = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def clean(self):
        """
        Validation:
        - If the type is not custom, the name cannot be changed
        - Check channels and variables for validity
        """
        allowed_channels = {"email", "telegram", "viber", "push"}
        if not set(self.channels).issubset(allowed_channels):
            raise ValidationError("Invalid channel in channels")


class NotificationTemplate(models.Model):
    type = models.ForeignKey(
        NotificationType,
        on_delete=models.CASCADE,
        related_name="templates"
    )

    channel = models.CharField(max_length=10, choices=NotificationType.CHANNEL_CHOICES)
    title = models.CharField(max_length=255, blank=True)
    html = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # For type != custom, only allow one template per type + channel
        unique_together = [('type', 'channel')]

    def __str__(self):
        return f"{self.type.name} - {self.channel}"

    def clean(self):
        """
        Validation:
        - title must be empty for telegram and viber
        - check html for allowed tags (later via validators)
        - check that all notification type variables are present in html
        """
        if self.channel in ["telegram", "viber"] and self.title:
            raise ValidationError("Title must be empty for telegram and viber")
