from django.core.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import NotificationType, NotificationTemplate
from .serializers import (
    NotificationTypeSerializer,
    NotificationTemplateSerializer,
)
from .permissions import IsAdminOrReadOnly


class NotificationTypeViewSet(ModelViewSet):
    queryset = NotificationType.objects.all()
    serializer_class = NotificationTypeSerializer
    permission_classes = [IsAdminOrReadOnly]


class NotificationTemplateViewSet(ModelViewSet):
    queryset = NotificationTemplate.objects.select_related("type")
    serializer_class = NotificationTemplateSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_destroy(self, instance):
        """
        Forbid deleting templates for non-custom notification types
        """
        if not instance.type.is_custom:
            raise ValidationError(
                "Deleting templates for non-custom notification types is not allowed."
            )

        instance.delete()
