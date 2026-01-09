import re
from django.core.exceptions import ValidationError


VARIABLE_PATTERN = re.compile(r"{{\s*(\w+)\s*}}")


def validate_variables(html: str, allowed_variables: list):
    """
    Checks:
    1. That there are no extra variables in the html
    2. That all required variables are present
    """

    # All variables actually used in the template
    used_variables = set(VARIABLE_PATTERN.findall(html))

    allowed_variables = set(allowed_variables or [])

    # Redundant variables
    extra_vars = used_variables - allowed_variables
    if extra_vars:
        raise ValidationError(
            f"Template contains invalid variables: {sorted(extra_vars)}"
        )

    # Missing required variables
    missing_vars = allowed_variables - used_variables
    if missing_vars:
        raise ValidationError(
            f"Template is missing required variables: {sorted(missing_vars)}"
        )

    return True
