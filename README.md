## Description

The system allows you to:

- Create notification types (for superuser).
- Create, edit and delete notification templates.
- Validate HTML templates:
  - Allowed HTML tags for each channel:
    - Email: `p`, `b`, `i`, `a`, `br`
    - Telegram, Viber: `p`, `br`
    - Push: no tags
  - Django Template correctness (`{% if %}`, `{{variable}}`)
  - Allowed variables (`variables`) are determined by the notification type
- Send notifications via channel abstractions (`BaseChannel`) and concrete implementations (`EmailChannel`, `TelegramChannel`, `ViberChannel`, `PushChannel`).

---

## Notification types

| Type                     | Channels               | Variables              | Features                     |
|--------------------------|----------------------|-----------------------|-------------------------------|
| new survey               | email, telegram, viber, push | title                 | One template per type          |
| confirm email            | email                 | confirmation_token    | One template per type          |
| bot successful subscribe | telegram, viber       | username              | One template per type          |
| custom                   | email, telegram, viber, push | -                     | User can add multiple templates |

> Deleting templates for types other than `custom` is not allowed.

---

## Project structure

```bash
django-notifications/
├─ config/
│  ├─ settings.py
│  ├─ urls.py
│  ├─ wsgi.py
│  ├─ asgi.py
│  └─ __init__.py
├─ db.sqlite3
├─ manage.py
├─ notifications/
│ ├─ migrations/
│ ├─ models.py
│ ├─ serializers.py
│ ├─ views.py
│ ├─ permissions.py
│ ├─ services/
│ │ ├─ channels/
│ │ │ ├─ base.py
│ │ │ ├─ email.py
│ │ │ ├─ telegram.py
│ │ │ ├─ viber.py
│ │ │ └─ push.py
│ │ └─ sender.py
│ └─ validations/
│ ├─ html.py
│ └─ variables.py
├─ requirements.txt 
```

---

## Installation

1. Create a virtual environment:

```bash
python -m venv .venv
source .venv/Scripts/activate
```


2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Make migrations and create a database:
```bash
python manage.py makemigrations
python manage.py migrate
```

# Usage

## Creating NotificationType and NotificationTemplate

```bash
from notifications.models import NotificationType, NotificationTemplate

email_type, _ = NotificationType.objects.get_or_create(
    name="confirm email",
    defaults={
        "channels": ["email"],
        "variables": ["confirmation_token"],
        "is_custom": False,
    }
)

template, _ = NotificationTemplate.objects.get_or_create(
    type=email_type,
    channel="email",
    defaults={
        "title": "Confirm your email",
        "html": "<p>Hello, please confirm your email: {{confirmation_token}}</p>",
    }
)
```

## Sending a notification

```bash
from notifications.services.sender import NotificationSender

sender = NotificationSender()
sender.send(
    notification_type=email_type,
    channel="email",
    recipient="test@example.com",
    context={"confirmation_token": "12345TOKEN"},
)
```

Similarly, you can test telegram, viber, push (while they are wet).


## API

NotificationTypeViewSet — CRUD for notification types (only superuser can create new ones)

NotificationTemplateViewSet — CRUD for notification templates (with HTML and variable validation)

## Notes

Used DRF (Django Rest Framework) for API.

HTML rendering via Django Template.

Ability to add new channels via BaseChannel implementation.