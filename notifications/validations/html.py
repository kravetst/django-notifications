from django.core.exceptions import ValidationError
from django.template import Template, TemplateSyntaxError
from bs4 import BeautifulSoup

# Per-channel tags allowed
ALLOWED_TAGS = {
    "email": {"p", "b", "i", "a", "br"},
    "telegram": {"p", "br"},
    "viber": {"p", "br"},
    "push": set(),  # no tags allowed
}


def validate_html(channel: str, html: str):
    """
    HTML validation for a specific channel.
    1. Only allowed tags.
    2. Django Template correctness.
    """
    if channel not in ALLOWED_TAGS:
        raise ValidationError(f"Unknown channel: {channel}")

    allowed = ALLOWED_TAGS[channel]

    # --- Tag validation ---
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(True):  # all tags
        if tag.name not in allowed:
            raise ValidationError(
                f"Tag <{tag.name}> is not allowed for channel '{channel}'"
            )

    # --- Django template validation ---
    try:
        Template(html)
    except TemplateSyntaxError as e:
        raise ValidationError(f"Invalid Django template: {str(e)}")

    # If everything is ok
    return True