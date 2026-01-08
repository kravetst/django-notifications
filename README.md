# Django Notifications System

This project implements a **notification system** for a Django application, designed to send messages via multiple channels (email, Telegram, Viber, push). It supports:

- Creation of **notification types** (e.g., new survey, confirm email)
- Creation and management of **notification templates** per type and channel
- Validation of templates for allowed HTML tags, Django template syntax, and variables
- Service layer (`NotificationService`) to send notifications to users
- Modular architecture for **adding new channels** easily
- Email channel fully implemented (other channels are abstract)

## Features

- **Superuser can:** add notification types, manage templates
- **Validation:** ensures templates are correct before saving
- **Extensible:** easy to add new channels or notification types
- **DRF API:** for managing types and templates

## Project Structure