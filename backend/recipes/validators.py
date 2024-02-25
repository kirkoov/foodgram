import re

from django.conf import settings
from django.core.exceptions import ValidationError


def validate_hex_color(value):
    hex_reg = re.compile(settings.HEX_FIELD_REQ)
    if not re.search(hex_reg, value):
        raise ValidationError("See the ReDoc for the hex field requirements.")


def validate_slug_field(value):
    slug_reg = re.compile(settings.SLUG_FIELD_REQ)
    if not re.search(slug_reg, value):
        raise ValidationError(
            "Check the ReDoc for the slug field requirements."
        )
