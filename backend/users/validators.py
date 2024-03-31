import regex as re
from backend.constants import USERNAME_FIELD_REQ
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


def is_email_valid(value):
    if validate_email(value) is False:
        raise ValidationError("See the ReDoc for the email requirements.")


def validate_username_field(value):
    username_reg = re.compile(USERNAME_FIELD_REQ)
    return re.search(username_reg, value)
    # if not re.search(username_reg, value):
    #     raise ValidationError(
    #         "Check the ReDoc for the username field requirements."
    #     )
